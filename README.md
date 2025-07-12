# 🤖 ScholarAgent - 智能科研论文分析助手

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![DeepSeek](https://img.shields.io/badge/DeepSeek-LLM-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**基于 ReAct 框架的智能科研 Agent，融合多源学术检索与 LLM 推理能力**

[🚀 快速开始](#-快速开始) • [📖 使用示例](#-使用示例) • [🏗️ 技术架构](#️-技术架构) • [🤝 贡献指南](#-贡献指南)

</div>

---

## 🎯 项目特色

### 🧠 智能 Agent 架构
- **ReAct 推理框架**：Reasoning-Acting-Observation 循环，实现复杂任务的分解与执行
- **任务规划模块**：基于 LLM 的智能任务分解器，支持多步推理链路
- **上下文记忆**：完整的对话历史与论文缓存，支持指代表达理解
- **工具链集成**：模块化设计，支持插件化扩展

### 🔍 多源学术检索
- **Arxiv 检索**：实时获取最新学术论文
- **Semantic Scholar**：深度学术数据挖掘
- **融合检索**：多源数据智能整合与去重
- **智能筛选**：基于关键词、作者、时间等多维度筛选

### 💡 智能分析能力
- **自动总结**：论文贡献、方法、创新点智能提取
- **智能问答**：基于论文内容的深度问答
- **论文比较**：多论文异同点分析
- **关键点提取**：核心信息快速定位

### 🎨 现代化界面
- **实时进度展示**：分步执行过程可视化
- **双界面支持**：命令行 + Web 界面
- **响应式设计**：适配多种设备
- **交互式体验**：直观的操作流程

---

## 🚀 前端界面展示

<div align="center">

> 📸 **界面截图展示区**
<img width="2406" height="1240" alt="image" src="https://github.com/user-attachments/assets/65825d19-c640-4d9e-8275-91b904b5bd2b" />


</div>

---

## 🏗️ 技术架构

### 核心架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    ScholarAgent 系统架构                      │
├─────────────────────────────────────────────────────────────┤
│  🎨 用户界面层 (UI Layer)                                    │
│  ├── Streamlit Web 界面                                      │
│  └── 命令行界面                                              │
├─────────────────────────────────────────────────────────────┤
│  🧠 Agent 控制层 (Agent Layer)                               │
│  ├── ReAct 控制器 (controller.py)                            │
│  ├── 任务规划器 (planner.py)                                 │
│  ├── 工具管理器 (tools.py)                                   │
│  └── 提示词模板 (prompts.py)                                 │
├─────────────────────────────────────────────────────────────┤
│  🔧 服务层 (Service Layer)                                   │
│  ├── Arxiv 搜索服务 (search.py)                              │
│  ├── Semantic Scholar 服务 (semantic_scholar.py)            │
│  └── LLM 总结服务 (summarize.py)                             │
├─────────────────────────────────────────────────────────────┤
│  🌐 数据源层 (Data Layer)                                    │
│  ├── Arxiv API                                              │
│  ├── Semantic Scholar API                                   │
│  └── DeepSeek LLM API                                       │
└─────────────────────────────────────────────────────────────┘
```

### 项目结构

```
ScholarAgent/
├── 📁 agent/                    # Agent 核心模块
│   ├── 🎮 controller.py        # ReAct Agent 控制器
│   ├── 🛠️ tools.py             # LangChain 工具定义
│   ├── 📋 planner.py           # 任务分解模块
│   └── 💬 prompts.py           # 提示词模板
├── 📁 services/                 # 服务层
│   ├── 🔍 search.py            # Arxiv 搜索服务
│   ├── 📚 semantic_scholar.py  # Semantic Scholar 检索
│   └── 📝 summarize.py         # LLM 总结服务
├── 📁 ui/                       # 用户界面
│   └── 🌐 streamlit_app.py     # Streamlit Web 界面
├── 📁 examples/                 # 使用示例
│   └── 📄 demo_run.md          # 演示文档
├── ⚙️ config.py                # 配置管理
├── 🚀 app.py                   # 命令行入口
├── 📋 requirements.txt         # 依赖包
├── 🚫 .gitignore               # Git 忽略文件
├── 🔧 env_example.txt          # 环境变量示例
└── 📖 README.md                # 项目文档
```

### 技术栈

| 技术组件 | 版本 | 用途 | 特点 |
|---------|------|------|------|
| **Python** | 3.8+ | 主要开发语言 | 简洁、生态丰富 |
| **LangChain** | 0.1.0+ | Agent 框架 | ReAct 推理、工具链 |
| **DeepSeek** | - | LLM 服务 | 强大的推理能力 |
| **Streamlit** | 1.28.1+ | Web 界面 | 快速开发、实时更新 |
| **Arxiv API** | - | 论文检索 | 实时、全面 |
| **Semantic Scholar** | - | 学术数据 | 深度、结构化 |

---

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8 或更高版本
- **DeepSeek API**: 有效的 API 密钥
- **网络**: 稳定的互联网连接
- **内存**: 建议 4GB+ RAM

### 🔧 安装配置

#### 1. 克隆项目
```bash
git clone https://github.com/LBJ-mlo/ScholarAgent.git
cd ScholarAgent
```

#### 2. 安装依赖
```bash
# 创建虚拟环境（推荐）
python -m venv scholaragent_env
source scholaragent_env/bin/activate  # Linux/Mac
# 或
scholaragent_env\Scripts\activate     # Windows

# 安装依赖包
pip install -r requirements.txt
```

#### 3. 配置环境变量
```bash
# 复制环境变量模板
cp env_example.txt .env

# 编辑 .env 文件，填入你的 API 密钥
```

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# 可选：代理配置（如需要）
# HTTP_PROXY=http://your-proxy:port
# HTTPS_PROXY=http://your-proxy:port
```

### 🎯 运行应用

#### 命令行模式
```bash
python app.py
```

#### Web 界面模式（推荐）
```bash
streamlit run ui/streamlit_app.py
```

访问 http://localhost:8501 开始使用！

---

## 📖 使用示例

### 🔍 基础论文检索

```python
from agent.controller import run_agent

# 搜索特定论文
result = run_agent("请搜索论文 Segment Anything")
print(result)

# 按作者搜索
result = run_agent("搜索作者 Yann LeCun 的最新论文")
print(result)

# 按关键词搜索
result = run_agent("搜索关于 'transformer' 的计算机视觉论文")
print(result)
```

### 📝 智能论文总结

```python
from agent.controller import create_scholar_agent

agent = create_scholar_agent()

# 总结论文贡献
result = agent.summarize_paper("Segment Anything")
print(result["answer"])

# 分析技术方法
result = agent.analyze_methods("Attention Is All You Need")
print(result["answer"])
```

### 💬 智能问答

```python
# 基于论文内容回答问题
result = agent.answer_question(
    "这篇论文的主要创新点是什么？", 
    "Segment Anything"
)
print(result["answer"])

# 多轮对话（支持指代表达）
result1 = agent.run("搜索论文 BERT")
result2 = agent.run("这篇论文的作者是谁？")  # 自动理解指代
result3 = agent.run("它的主要贡献是什么？")
```

### 🔄 论文比较分析

```python
# 比较两篇论文
result = agent.compare_papers(
    "Segment Anything", 
    "Attention Is All You Need"
)
print(result["answer"])
```

### 🎯 复杂任务分解

```python
# 复合型任务（自动分解执行）
result = agent.run("""
请按以下步骤分析：
1. 搜索关于 'vision transformer' 的最新论文
2. 总结其中最重要的3篇论文
3. 比较它们的异同点
4. 给出研究趋势分析
""")
```

---

## 🎨 功能演示

### 分步执行过程

当你在 Web 界面输入复杂任务时，系统会：

1. **任务分解**：将复杂任务拆分为多个子任务
2. **逐步执行**：按顺序执行每个子任务
3. **实时展示**：前端实时显示执行进度和结果
4. **结果整合**：将所有结果整合为最终答案

### 多源检索结果

系统会同时从多个数据源检索信息：

- **Arxiv**：获取最新预印本论文
- **Semantic Scholar**：获取结构化学术数据
- **智能融合**：去重、排序、整合结果

---

## 🔧 高级配置

### 自定义工具链

```python
from agent.tools import create_custom_tool

# 创建自定义工具
@create_custom_tool
def custom_search_tool(query: str) -> str:
    """自定义搜索工具"""
    # 实现你的搜索逻辑
    return "搜索结果"
```

### 调整 Agent 参数

```python
from agent.controller import create_scholar_agent

# 创建自定义 Agent
agent = create_scholar_agent(
    max_iterations=10,      # 最大迭代次数
    temperature=0.7,        # 创造性参数
    verbose=True           # 详细输出
)
```

---

## 🚀 部署选项

### 本地部署
```bash
# 直接运行
python app.py

# 后台运行
nohup python app.py > app.log 2>&1 &
```

### Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 云平台部署

- **Streamlit Cloud**：一键部署 Web 应用
- **Heroku**：支持 Procfile 部署
- **Vercel**：支持 Python 应用部署
- **AWS/GCP**：容器化部署

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 🐛 报告问题

如果你发现了 bug 或有功能建议，请：

1. 查看 [现有 Issues](https://github.com/LBJ-mlo/ScholarAgent/issues)
2. 创建新的 Issue，详细描述问题
3. 提供复现步骤和环境信息

### 💡 提交代码

1. **Fork** 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 **Pull Request**

### 📝 代码规范

- 遵循 PEP 8 代码风格
- 添加适当的注释和文档
- 确保代码通过测试
- 更新相关文档

---


## 🙏 致谢

感谢以下开源项目和服务：

- **[LangChain](https://github.com/langchain-ai/langchain)** - 优秀的 Agent 框架
- **[DeepSeek](https://www.deepseek.com/)** - 强大的 LLM 服务
- **[Arxiv](https://arxiv.org/)** - 开放的论文平台
- **[Semantic Scholar](https://www.semanticscholar.org/)** - 深度学术数据
- **[Streamlit](https://streamlit.io/)** - 便捷的 Web 框架

---

## 📞 联系我们

- **GitHub Issues**: [提交问题](https://github.com/LBJ-mlo/ScholarAgent/issues)
- **项目主页**: [https://github.com/LBJ-mlo/ScholarAgent](https://github.com/LBJ-mlo/ScholarAgent)
- **邮箱**: 3195526804@qq.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我们一个 Star！**

Made with ❤️ by [LBJ-mlo](https://github.com/LBJ-mlo)

</div> 
