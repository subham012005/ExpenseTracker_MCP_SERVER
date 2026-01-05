# 💰 ExpenseTracker MCP Server

**GitHub:** https://github.com/subham012005/ExpenseTracker_MCP_SERVER

Minimal Model Context Protocol (MCP) server for expense tracking using **FastMCP**, **SQLite**, and **aiosqlite** — exposes tools and a resource for AI assistants to add, list, and summarize expenses. :contentReference[oaicite:0]{index=0}

---

## 📌 Overview

This repository implements a lightweight MCP server to:

- Insert expense records
- Query expenses by date range
- Summarize spending by category
- Serve default categories via MCP resource

All logic runs over an SQLite database stored in system temp directory.

---

## ✨ Features

- Async tools for MCP
- Auto DB initialization
- Expense adding & querying
- Category resource backed by JSON
- Simple, dependency-minimal design

---

## ⚙️ Setup & Installation

### 1️⃣ Clone

```bash
git clone https://github.com/subham012005/ExpenseTracker_MCP_SERVER.git
cd ExpenseTracker_MCP_SERVER
```
### 2️⃣ Install uv
macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows (PowerShell)
```bash
irm https://astral.sh/uv/install.ps1 | iex
```
then check in termainl
```bash
uv --version
```

3️⃣ Install dependencies
```bash
uv add install fastmcp aiosqlite
```
4️⃣ Run
```bash
uv run fastmcp dev main.py
```

## DB and tables initialize automatically on first run.

## 🚀 Tools (MCP)

### ➕ add_expense
Add an expense entry.

**Params**
- `date`
- `amount`
- `category`
- `subcategory` (optional)
- `note` (optional)

**Returns**
- Success or error JSON

---

### 📄 list_expenses
Retrieve expenses between `start_date` and `end_date`.

**Returns**
- List of expense objects

---

### 📊 summarize
Category-wise summary of total spend.

**Params**
- `start_date`
- `end_date`
- `category` (optional)

**Returns**
- Aggregated totals

---

## 📦 Resource

### expense:///categories
Serves expense categories in JSON format.
- Loads from custom file if present
- Falls back to default categories

---

## 🛠️ Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit and push changes  
4. Open a Pull Request  
