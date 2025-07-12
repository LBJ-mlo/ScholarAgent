"""
Agent提示词模板模块

该模块定义了ScholarAgent使用的各种提示词模板，
包括系统提示词、任务提示词等。
"""

from langchain.prompts import PromptTemplate

# ReAct Agent系统提示词模板
REACT_SYSTEM_PROMPT = """你是一个专业的科研论文分析助手ScholarAgent。你的任务是帮助用户检索、分析和理解科研论文。

你的能力包括：
1. 通过Arxiv API检索论文
2. 分析论文的研究贡献和技术方法
3. 回答用户关于论文的具体问题
4. 比较不同论文的异同点
5. 生成论文的关键信息点

重要提示：
- 请仔细阅读对话历史中的上下文信息
- 如果用户询问之前搜索过的论文的详细信息，请基于已缓存的信息回答
- 如果缓存中没有相关信息，再使用工具进行搜索
- 保持对话的连贯性，理解用户的指代（如"这篇论文"、"作者"等）
- **在输出论文信息时，务必包含arXiv ID和PDF链接，方便用户查阅原文**

工作流程：
1. 理解用户需求，结合对话历史
2. 选择合适的工具执行任务
3. 分析结果并给出专业回答
4. 提供清晰、准确的中文回答

请始终保持专业、客观的态度，基于论文内容进行回答。

可用工具：
{tool_names}

{tools}

请按照以下格式回答：
Question: 用户问题
Thought: 思考过程
Action: 工具名称
Action Input: 工具输入
Observation: 工具输出
... (可以重复多次)
Thought: 最终思考
Final Answer: 最终答案

请用中文回答。"""

# 任务分析提示词
TASK_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["user_input"],
    template="""请分析用户输入，确定需要执行的任务类型：

用户输入: {user_input}

请从以下任务类型中选择：
1. SEARCH_PAPER - 搜索论文（当用户提到论文名称、作者或关键词时）
2. SUMMARIZE_CONTRIBUTIONS - 总结研究贡献（当用户要求总结论文贡献时）
3. SUMMARIZE_METHODS - 总结技术方法（当用户要求分析技术方法时）
4. ANSWER_QUESTION - 回答问题（当用户提出具体问题时）
5. COMPARE_PAPERS - 比较论文（当用户要求比较多篇论文时）
6. GENERATE_KEY_POINTS - 生成关键点（当用户要求提取关键信息时）

请只返回任务类型名称，不要其他内容。"""
)

# 论文搜索提示词
SEARCH_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""请分析用户查询，确定搜索策略：

用户查询: {query}

请确定：
1. 搜索类型：title（按标题）、keywords（按关键词）、author（按作者）
2. 搜索关键词：提取最相关的搜索词

格式：搜索类型:关键词

例如：
- title:Segment Anything
- keywords:machine learning computer vision
- author:Yann LeCun"""
)

# 总结提示词
SUMMARIZE_PROMPT = PromptTemplate(
    input_variables=["paper_info", "summary_type"],
    template="""请基于以下论文信息进行{summary_type}分析：

论文信息：
{paper_info}

请提供专业、准确的分析，用中文回答。"""
)

# 问答提示词
QA_PROMPT = PromptTemplate(
    input_variables=["question", "paper_info"],
    template="""请基于以下论文信息回答用户问题：

论文信息：
{paper_info}

用户问题：{question}

请基于论文内容准确回答，如果论文中没有相关信息，请明确说明。用中文回答。"""
)

# 比较分析提示词
COMPARE_PROMPT = PromptTemplate(
    input_variables=["paper1_info", "paper2_info"],
    template="""请比较分析以下两篇论文：

论文A：
{paper1_info}

论文B：
{paper2_info}

请从研究问题、技术方法、创新点、优缺点、应用场景等角度进行比较分析。用中文回答。"""
)

# 关键点提取提示词
KEY_POINTS_PROMPT = PromptTemplate(
    input_variables=["paper_info"],
    template="""请从以下论文信息中提取关键点：

论文信息：
{paper_info}

请提取以下类型的关键点：
1. 研究问题
2. 主要方法
3. 创新点
4. 实验结果
5. 应用价值

每个关键点用一句话概括，用中文表达。"""
)

# 错误处理提示词
ERROR_PROMPT = PromptTemplate(
    input_variables=["error_message", "user_input"],
    template="""抱歉，在处理您的请求时遇到了问题：

错误信息：{error_message}
用户输入：{user_input}

请尝试：
1. 重新表述您的问题
2. 提供更具体的论文名称或关键词
3. 检查网络连接

如果问题持续存在，请稍后重试。"""
)

# 结果格式化提示词
FORMAT_RESULT_PROMPT = PromptTemplate(
    input_variables=["result", "task_type"],
    template="""请将以下{task_type}结果格式化为用户友好的回答：

原始结果：
{result}

请：
1. 保持专业性和准确性
2. 使用清晰的中文表达
3. 结构化和易读的格式
4. 突出重要信息"""
)

# 工具选择提示词
TOOL_SELECTION_PROMPT = PromptTemplate(
    input_variables=["available_tools", "user_input"],
    template="""请根据用户输入选择合适的工具：

可用工具：
{available_tools}

用户输入：{user_input}

请选择最合适的工具，并说明选择理由。"""
)

# 多轮对话提示词
CONVERSATION_PROMPT = PromptTemplate(
    input_variables=["conversation_history", "current_input"],
    template="""请基于对话历史回答当前问题：

对话历史：
{conversation_history}

当前问题：{current_input}

请：
1. 理解对话上下文
2. 保持回答的一致性
3. 如果需要，可以引用之前的讨论
4. 用中文回答"""
) 