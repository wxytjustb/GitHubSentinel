import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径



with gr.Blocks() as demo:
    gr.Markdown("# GitHubSentinel")  # 界面标题

    with gr.Row():
        new_subscription_input = gr.Textbox(label="添加新的订阅", placeholder="输入新的 GitHub 项目名称")
        add_subscription_button = gr.Button("添加订阅")

    with gr.Row():
        choices = subscription_manager.list_subscriptions()
        subscription_dropdown = gr.Dropdown(
            choices,
            value=choices[0],
            label="订阅列表",
            info="已订阅GitHub项目"
        )


        report_period_slider = gr.Slider(
            value=2,
            minimum=1,
            maximum=7,
            step=1,
            label="报告周期",
            info="生成项目过去一段时间进展，单位：天"
        )

    output_markdown = gr.Markdown(label="报告内容")
    output_file = gr.File(label="下载报告")


    def on_add_subscription_click(new_subscription):
        subscription_manager.add_subscription(new_subscription)
        updated_subscriptions = subscription_manager.list_subscriptions()
        subscription_dropdown.choices = [(item, item) for item in updated_subscriptions]
        subscription_dropdown.value = new_subscription
        return subscription_dropdown


    add_subscription_button.click(
        fn=on_add_subscription_click,
        inputs=[new_subscription_input],
        outputs=subscription_dropdown,
    )

    gr.Button("生成报告").click(
        export_progress_by_date_range,
        inputs=[subscription_dropdown, report_period_slider],
        outputs=[output_markdown, output_file],
    )


if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))