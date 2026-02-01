---
description: 產生 Logging 程式碼（根據技術棧）
---

## 🎯 目的
根據 `docs/tech-stack.md` 的技術棧設定，產生對應語言的 logging 程式碼，包含 SQLite handler。

## ⚠️ 重要原則
- **讀取 docs/tech-stack.md**：根據技術棧決定要產生哪些語言的 logging 程式碼
- **統一 log 格式**：`[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message`
- **三種輸出**：stdout/stderr、文字檔案、SQLite

## 🔗 執行順序
此 workflow 是初始化流程的可選步驟：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ✅
3. `/setup-structure` - 建立 src/ 目錄結構 ✅
4. `/setup-logging` - 產生 logging 程式碼 ← 你在這裡
5. `/setup-agents` - 建立 AGENTS.md
6. `/setup-makefile` - 建立 Makefile（可選）

---

## 📋 執行步驟

### 1. 讀取技術棧設定
// turbo
```bash
cat docs/tech-stack.md
```

根據 `docs/tech-stack.md` 的 Logging 區塊，判斷需要產生哪些語言的程式碼。

### 2. 產生 Python logging 程式碼（如果使用 Python）

**檢查是否使用 Python：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "Python" in tech_stack or "python" in tech_stack:
    print("🐍 需要產生 Python logging 程式碼")
else:
    print("⏭️ 不使用 Python，跳過")
```

**如果使用 Python，產生以下檔案：**

#### `src/shared/logging/__init__.py`
```python
from .logger import get_logger, setup_logging

__all__ = ["get_logger", "setup_logging"]
```

#### `src/shared/logging/logger.py`
```python
"""
統一 Logging 模組

Log 格式：[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message
輸出目標：stdout/stderr、文字檔案、SQLite
"""
import sys
from pathlib import Path
from loguru import logger

from .sqlite_handler import SQLiteHandler

# 預設 log 目錄
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 統一格式
LOG_FORMAT = "[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [{name}] {message}"


def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
    sqlite_file: str | None = None,
) -> None:
    """
    設定 logging
    
    Args:
        level: Log 等級 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 文字 log 檔案路徑，預設為 src/logs/app.log
        sqlite_file: SQLite log 檔案路徑，預設為 src/logs/app.log.db
    """
    # 移除預設 handler
    logger.remove()
    
    # stdout/stderr
    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        level=level,
        colorize=True,
    )
    
    # 文字檔案
    if log_file is None:
        log_file = LOG_DIR / "app.log"
    logger.add(
        log_file,
        format=LOG_FORMAT,
        level=level,
        rotation="00:00",  # 每日 rotate
        retention="30 days",
        encoding="utf-8",
    )
    
    # SQLite
    if sqlite_file is None:
        sqlite_file = LOG_DIR / "app.log.db"
    sqlite_handler = SQLiteHandler(sqlite_file)
    logger.add(
        sqlite_handler.write,
        format=LOG_FORMAT,
        level=level,
    )


def get_logger(name: str):
    """
    取得 logger 實例
    
    Args:
        name: 模組名稱
        
    Returns:
        綁定模組名稱的 logger
    """
    return logger.bind(name=name)
```

#### `src/shared/logging/sqlite_handler.py`
```python
"""
SQLite Log Handler

將 log 寫入 SQLite 資料庫，方便 AI debug 查詢。
"""
import sqlite3
import threading
from datetime import datetime
from pathlib import Path


class SQLiteHandler:
    """SQLite Log Handler"""
    
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._init_db()
    
    def _get_conn(self) -> sqlite3.Connection:
        """取得 thread-local 的資料庫連線"""
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(str(self.db_path))
        return self._local.conn
    
    def _init_db(self) -> None:
        """初始化資料庫結構"""
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                logger TEXT NOT NULL,
                message TEXT NOT NULL,
                file TEXT,
                line INTEGER,
                function TEXT,
                context TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_level ON logs(level)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_logger ON logs(logger)")
        conn.commit()
    
    def write(self, message) -> None:
        """
        寫入 log 到 SQLite
        
        Args:
            message: loguru 的 message 物件
        """
        record = message.record
        conn = self._get_conn()
        conn.execute(
            """
            INSERT INTO logs (timestamp, level, logger, message, file, line, function)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["time"].isoformat(),
                record["level"].name,
                record.get("extra", {}).get("name", record["name"]),
                record["message"],
                record["file"].path if record["file"] else None,
                record["line"],
                record["function"],
            ),
        )
        conn.commit()
```

### 3. 產生 TypeScript logging 程式碼（如果使用 TypeScript）

**檢查是否使用 TypeScript：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "TypeScript" in tech_stack or "Node.js" in tech_stack or "React" in tech_stack or "Vue" in tech_stack:
    print("📦 需要產生 TypeScript logging 程式碼")
else:
    print("⏭️ 不使用 TypeScript，跳過")
```

**如果使用 TypeScript，產生以下檔案：**

#### `src/shared/logging/index.ts`
```typescript
export { logger, setupLogging, getLogger } from './logger';
```

#### `src/shared/logging/logger.ts`
```typescript
/**
 * 統一 Logging 模組
 * 
 * Log 格式：[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message
 * 輸出目標：stdout/stderr、文字檔案、SQLite
 */
import winston from 'winston';
import path from 'path';
import { SQLiteTransport } from './sqlite-transport';

const LOG_DIR = path.join(__dirname, '../../logs');

// 統一格式
const logFormat = winston.format.printf(({ level, message, timestamp, module }) => {
  return `[${timestamp}] [${level.toUpperCase()}] [${module || 'app'}] ${message}`;
});

// 建立 logger
export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    logFormat
  ),
  transports: [
    // Console
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
        logFormat
      ),
    }),
  ],
});

/**
 * 設定 logging
 */
export function setupLogging(options: {
  level?: string;
  logFile?: string;
  sqliteFile?: string;
} = {}): void {
  const { level = 'info', logFile, sqliteFile } = options;
  
  logger.level = level;
  
  // 文字檔案
  logger.add(new winston.transports.File({
    filename: logFile || path.join(LOG_DIR, 'app.log'),
    maxsize: 10 * 1024 * 1024, // 10MB
    maxFiles: 30,
  }));
  
  // SQLite
  logger.add(new SQLiteTransport({
    filename: sqliteFile || path.join(LOG_DIR, 'app.log.db'),
  }));
}

/**
 * 取得綁定模組名稱的 logger
 */
export function getLogger(moduleName: string) {
  return logger.child({ module: moduleName });
}
```

#### `src/shared/logging/sqlite-transport.ts`
```typescript
/**
 * SQLite Transport for Winston
 * 
 * 將 log 寫入 SQLite 資料庫，方便 AI debug 查詢。
 */
import Transport from 'winston-transport';
import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

interface SQLiteTransportOptions extends Transport.TransportStreamOptions {
  filename: string;
}

export class SQLiteTransport extends Transport {
  private db: Database.Database;
  private insertStmt: Database.Statement;

  constructor(opts: SQLiteTransportOptions) {
    super(opts);
    
    // 確保目錄存在
    const dir = path.dirname(opts.filename);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    this.db = new Database(opts.filename);
    this.initDb();
    this.insertStmt = this.db.prepare(`
      INSERT INTO logs (timestamp, level, logger, message, file, line, function)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
  }

  private initDb(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        level TEXT NOT NULL,
        logger TEXT NOT NULL,
        message TEXT NOT NULL,
        file TEXT,
        line INTEGER,
        function TEXT,
        context TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp);
      CREATE INDEX IF NOT EXISTS idx_level ON logs(level);
      CREATE INDEX IF NOT EXISTS idx_logger ON logs(logger);
    `);
  }

  log(info: any, callback: () => void): void {
    setImmediate(() => {
      this.emit('logged', info);
    });

    const { level, message, timestamp, module } = info;
    
    this.insertStmt.run(
      timestamp || new Date().toISOString(),
      level.toUpperCase(),
      module || 'app',
      message,
      null, // file
      null, // line
      null  // function
    );

    callback();
  }

  close(): void {
    this.db.close();
  }
}
```

### 4. 產生 Rust logging 程式碼（如果使用 Rust）

**檢查是否使用 Rust：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "Rust" in tech_stack and "無" not in tech_stack.split("Rust")[1][:50]:
    print("🦀 需要產生 Rust logging 程式碼")
else:
    print("⏭️ 不使用 Rust，跳過")
```

**如果使用 Rust，產生以下檔案：**

#### `src/shared/logging/mod.rs`
```rust
//! 統一 Logging 模組
//!
//! Log 格式：[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message
//! 輸出目標：stdout/stderr、文字檔案、SQLite

mod sqlite_layer;

pub use sqlite_layer::SqliteLayer;

use tracing_subscriber::{
    fmt::{self, time::FormatTime},
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};
use std::path::Path;

/// 設定 logging
pub fn setup_logging(log_dir: &Path) -> anyhow::Result<()> {
    let log_file = log_dir.join("app.log");
    let sqlite_file = log_dir.join("app.log.db");
    
    // 建立目錄
    std::fs::create_dir_all(log_dir)?;
    
    // 檔案 appender
    let file_appender = tracing_appender::rolling::daily(log_dir, "app.log");
    
    // SQLite layer
    let sqlite_layer = SqliteLayer::new(&sqlite_file)?;
    
    // 組合 subscriber
    tracing_subscriber::registry()
        .with(EnvFilter::from_default_env().add_directive(tracing::Level::INFO.into()))
        .with(
            fmt::layer()
                .with_timer(CustomTimer)
                .with_target(true)
        )
        .with(
            fmt::layer()
                .with_timer(CustomTimer)
                .with_target(true)
                .with_ansi(false)
                .with_writer(file_appender)
        )
        .with(sqlite_layer)
        .init();
    
    Ok(())
}

/// 自訂時間格式
struct CustomTimer;

impl FormatTime for CustomTimer {
    fn format_time(&self, w: &mut fmt::format::Writer<'_>) -> std::fmt::Result {
        let now = chrono::Local::now();
        write!(w, "{}", now.format("%Y-%m-%d %H:%M:%S"))
    }
}
```

#### `src/shared/logging/sqlite_layer.rs`
```rust
//! SQLite Layer for tracing
//!
//! 將 log 寫入 SQLite 資料庫，方便 AI debug 查詢。

use rusqlite::{Connection, params};
use std::path::Path;
use std::sync::Mutex;
use tracing::Subscriber;
use tracing_subscriber::Layer;

pub struct SqliteLayer {
    conn: Mutex<Connection>,
}

impl SqliteLayer {
    pub fn new(db_path: &Path) -> anyhow::Result<Self> {
        let conn = Connection::open(db_path)?;
        
        conn.execute(
            "CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                logger TEXT NOT NULL,
                message TEXT NOT NULL,
                file TEXT,
                line INTEGER,
                function TEXT,
                context TEXT
            )",
            [],
        )?;
        
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)", [])?;
        conn.execute("CREATE INDEX IF NOT EXISTS idx_level ON logs(level)", [])?;
        conn.execute("CREATE INDEX IF NOT EXISTS idx_logger ON logs(logger)", [])?;
        
        Ok(Self {
            conn: Mutex::new(conn),
        })
    }
    
    fn write_log(&self, level: &str, target: &str, message: &str) {
        let timestamp = chrono::Local::now().to_rfc3339();
        
        if let Ok(conn) = self.conn.lock() {
            let _ = conn.execute(
                "INSERT INTO logs (timestamp, level, logger, message) VALUES (?1, ?2, ?3, ?4)",
                params![timestamp, level, target, message],
            );
        }
    }
}

impl<S: Subscriber> Layer<S> for SqliteLayer {
    fn on_event(
        &self,
        event: &tracing::Event<'_>,
        _ctx: tracing_subscriber::layer::Context<'_, S>,
    ) {
        let level = event.metadata().level().as_str();
        let target = event.metadata().target();
        
        // 簡單的 message 提取
        let mut visitor = MessageVisitor::default();
        event.record(&mut visitor);
        
        self.write_log(level, target, &visitor.message);
    }
}

#[derive(Default)]
struct MessageVisitor {
    message: String,
}

impl tracing::field::Visit for MessageVisitor {
    fn record_debug(&mut self, field: &tracing::field::Field, value: &dyn std::fmt::Debug) {
        if field.name() == "message" {
            self.message = format!("{:?}", value);
        }
    }
    
    fn record_str(&mut self, field: &tracing::field::Field, value: &str) {
        if field.name() == "message" {
            self.message = value.to_string();
        }
    }
}
```

### 5. 更新 .gitignore

// turbo
```python
from pathlib import Path

gitignore_path = Path(".gitignore")
gitignore_content = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""

log_ignores = """
# Logs
src/logs/*.log
src/logs/*.db
src/logs/archive/
"""

if "src/logs/" not in gitignore_content:
    with open(gitignore_path, "a", encoding="utf-8") as f:
        f.write(log_ignores)
    print("✅ 已更新 .gitignore")
else:
    print("⏭️ .gitignore 已包含 log 規則")
```

### 6. 驗證結構
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

print("🔍 驗證 logging 檔案...")

files_to_check = []

if "Python" in tech_stack or "python" in tech_stack:
    files_to_check.extend([
        "src/shared/logging/__init__.py",
        "src/shared/logging/logger.py",
        "src/shared/logging/sqlite_handler.py",
    ])

if "TypeScript" in tech_stack or "Node.js" in tech_stack:
    files_to_check.extend([
        "src/shared/logging/index.ts",
        "src/shared/logging/logger.ts",
        "src/shared/logging/sqlite-transport.ts",
    ])

if "Rust" in tech_stack:
    files_to_check.extend([
        "src/shared/logging/mod.rs",
        "src/shared/logging/sqlite_layer.rs",
    ])

all_ok = True
for f in files_to_check:
    if Path(f).exists():
        print(f"✅ {f}")
    else:
        print(f"❌ {f} (不存在)")
        all_ok = False

if all_ok:
    print("\n✅ 所有 logging 檔案已建立")
else:
    print("\n⚠️ 部分檔案未建立，請檢查")
```

### 7. 顯示完成訊息
執行完成後，輸出以下訊息：
```
✅ Logging 程式碼產生完成！

已建立的檔案：
📄 src/shared/logging/ - Logging 程式碼
📄 .gitignore - 已更新 log 規則

Log 規格：
- 格式：[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message
- 輸出：stdout/stderr、文字檔案、SQLite
- 保留：30 天

下一步：
  - 執行 `/setup-agents` 建立 AGENTS.md
  - 或執行 `/setup-makefile` 建立 Makefile
```

## 📝 注意事項

1. 此 workflow 會根據 `docs/tech-stack.md` 動態產生對應語言的程式碼
2. 已存在的檔案不會被覆蓋
3. 如果 `docs/tech-stack.md` 不存在，請先執行 `/setup-techstack`
4. 如果 `src/shared/logging/` 目錄不存在，請先執行 `/setup-structure`

## 🔧 依賴套件

執行此 workflow 後，需要安裝以下依賴：

**Python:**
```bash
pip install loguru
```

**TypeScript:**
```bash
npm install winston better-sqlite3
npm install -D @types/better-sqlite3
```

**Rust (Cargo.toml):**
```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
tracing-appender = "0.2"
rusqlite = { version = "0.31", features = ["bundled"] }
chrono = "0.4"
anyhow = "1.0"
```

## 🔗 相關文件

- `docs/logging-strategy.md` - Logging 策略說明
- `docs/tech-stack.md` - 技術棧設定
