# ScholarAgent - 智能科研论文分析助手

---

## 🚀 前端界面展示

![Uploading image.png…]()


---

## 项目简介

ScholarAgent 是一个基于 LangChain ReAct 框架的智能科研论文分析助手，集成 DeepSeek 大语言模型，支持论文检索、自动总结、智能问答、论文比较、任务分解与多源学术检索等功能，适用于科研人员、学生和学术工作者。

---

## 主要功能亮点

- **分步任务规划与执行**：支持复杂学术任务的自动分解与实时分步执行，前端可实时展示每步进度。
- **多源学术检索**：融合 Arxiv、Semantic Scholar 等多源学术API，提升检索全面性。
- **智能总结与问答**：自动总结论文贡献、方法、创新点，支持基于论文内容的智能问答。
- **论文比较与关键点提取**：支持多论文异同点分析与关键信息提取。
- **上下文记忆与多轮对话**：支持多轮对话、指代表达理解和论文缓存。
- **现代化Web界面**：基于Streamlit，支持实时进度展示、分步执行过程可视化。

---

## 技术架构

```
ScholarAgent/
├── agent/                 # Agent核心模块
│   ├── controller.py     # ReAct Agent控制器
│   ├── tools.py          # LangChain工具定义
│   ├── planner.py        # 任务分解模块
│   └── prompts.py        # 提示词模板
├── services/             # 服务层
│   ├── search.py         # Arxiv搜索服务
│   ├── semantic_scholar.py # Semantic Scholar检索
│   └── summarize.py      # LLM总结服务
├── ui/                   # 用户界面
│   └── streamlit_app.py  # Streamlit Web界面
├── config.py            # 配置管理
├── app.py               # 命令行入口
├── requirements.txt     # 依赖包
├── .gitignore           # Git忽略文件
├── env_example.txt      # 环境变量示例
└── README.md            # 项目文档
```

---

## 快速开始

### 1. 环境要求
- Python 3.8+
- DeepSeek API密钥
- 稳定的网络连接

### 2. 安装配置
```bash
# 克隆项目
git clone https://github.com/LBJ-mlo/ScholarAgent.git
cd ScholarAgent

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env_example.txt .env
# 编辑 .env 文件，填入API密钥
```

### 3. 运行应用
```bash
# 命令行模式
python app.py

# Web界面模式（推荐）
streamlit run ui/streamlit_app.py
```

---

## 使用示例

### 论文检索
```python
from agent.controller import run_agent
result = run_agent("请搜索论文 Segment Anything")
print(result)
```

### 智能总结
```python
from agent.controller import create_scholar_agent
agent = create_scholar_agent()
result = agent.summarize_paper("Segment Anything")
print(result["answer"])
```

### 分步任务与实时进度
- 在Web界面输入复合型任务（如“请先检索，再总结，再比较……”），可实时看到每步执行进度和结果。

---

## 贡献指南

欢迎任何形式的贡献！
1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建Pull Request

如有问题或建议，请在[GitHub Issues](https://github.com/LBJ-mlo/ScholarAgent/issues)留言。

---

## 许可证

本项目采用MIT许可证，详见 LICENSE 文件。

---

## 致谢
- LangChain团队
- DeepSeek团队
- Arxiv团队
- Semantic Scholar团队
- Streamlit团队

---

**⭐ 如果本项目对你有帮助，请Star支持！** 
