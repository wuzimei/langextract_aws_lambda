"""
本地测试脚本

用于在本地环境测试 Lambda 函数，无需部署到 AWS
"""

import json
import os
from lambda_function import lambda_handler


def test_basic_extraction():
    """测试基本的信息提取功能"""
    
    # 确保设置了 API Key
    if not os.environ.get('GEMINI_API_KEY'):
        print("错误: 请先设置 GEMINI_API_KEY 环境变量")
        print("示例: export GEMINI_API_KEY='your-api-key'")
        return
    
    # 模拟 API Gateway 事件
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'text': '''
            张三，男，45岁，患有高血压，服用降压药。
            李四，女，32岁，患有糖尿病，注射胰岛素。
            王五，男，28岁，健康，无慢性疾病。
            ''',
            'prompt': '提取每个人的姓名、年龄、性别和健康状况',
            'examples': [
                {
                    'name': '张三',
                    'age': 45,
                    'gender': '男',
                    'health_condition': '高血压'
                }
            ],
            'model_id': 'gemini-2.0-flash-exp',
            'chunk_size': 15000
        })
    }
    
    # 模拟 Lambda 上下文（简化版）
    class Context:
        function_name = "langextract-function"
        memory_limit_in_mb = 1024
        invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:langextract-function"
        aws_request_id = "test-request-id"
    
    context = Context()
    
    print("=" * 60)
    print("开始测试 Lambda 函数...")
    print("=" * 60)
    
    # 调用 Lambda 函数
    response = lambda_handler(event, context)
    
    # 打印结果
    print(f"\n状态码: {response['statusCode']}")
    print(f"\nHeaders: {json.dumps(response['headers'], indent=2, ensure_ascii=False)}")
    
    body = json.loads(response['body'])
    print(f"\n响应体:")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    
    # 验证结果
    if response['statusCode'] == 200 and body.get('success'):
        print("\n✅ 测试成功!")
        print(f"提取了 {body['metadata']['total_extractions']} 条记录")
    else:
        print("\n❌ 测试失败!")
        if 'error' in body:
            print(f"错误信息: {body['error']}")


def test_error_handling():
    """测试错误处理"""
    
    print("\n" + "=" * 60)
    print("测试错误处理...")
    print("=" * 60)
    
    # 测试缺少必需参数
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'prompt': '提取信息'
            # 缺少 text 参数
        })
    }
    
    class Context:
        function_name = "langextract-function"
    
    response = lambda_handler(event, Context())
    body = json.loads(response['body'])
    
    print(f"\n缺少 text 参数测试:")
    print(f"状态码: {response['statusCode']}")
    print(f"错误信息: {body.get('error')}")
    
    if response['statusCode'] == 400:
        print("✅ 错误处理正确")
    else:
        print("❌ 错误处理异常")


if __name__ == '__main__':
    print("LangExtract Lambda 函数本地测试")
    print("=" * 60)
    
    # 运行测试
    test_basic_extraction()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

