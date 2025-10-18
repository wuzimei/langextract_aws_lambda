"""
AWS Lambda 函数：LangExtract 信息提取服务

此函数接收 API Gateway 的 HTTP 请求，使用 langextract 进行文本信息提取，
并返回结构化的提取结果。
"""

import json
import os
import traceback
import langextract as lx


def lambda_handler(event, context):
    """
    Lambda 函数入口点
    
    参数:
        event (dict): API Gateway 事件对象
        context (object): Lambda 上下文对象
    
    返回:
        dict: API Gateway 响应格式
    """
    
    try:
        # 解析请求体
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # 从环境变量获取 API Key
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return create_response(
                400, 
                {'error': 'GEMINI_API_KEY 环境变量未设置'}
            )
        
        # 获取必需参数
        text_or_documents = body.get('text')
        prompt_description = body.get('prompt')
        examples = body.get('examples', [])
        
        # 验证必需参数
        if not text_or_documents:
            return create_response(
                400,
                {'error': '缺少必需参数: text'}
            )
        
        if not prompt_description:
            return create_response(
                400,
                {'error': '缺少必需参数: prompt'}
            )
        
        # 获取可选参数
        model_id = body.get('model_id', 'gemini-2.0-flash-exp')
        chunk_size = body.get('chunk_size', 15000)
        chunk_overlap = body.get('chunk_overlap', 100)
        max_threads = body.get('max_threads', 8)
        fence_output = body.get('fence_output', False)
        use_schema_constraints = body.get('use_schema_constraints', True)
        
        # 调用 langextract
        print(f"开始处理请求 - 模型: {model_id}, 文本长度: {len(text_or_documents)}")
        
        result = lx.extract(
            text_or_documents=text_or_documents,
            prompt_description=prompt_description,
            examples=examples,
            model_id=model_id,
            api_key=api_key,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            max_threads=max_threads,
            fence_output=fence_output,
            use_schema_constraints=use_schema_constraints
        )
        
        print(f"提取完成 - 结果数量: {len(result.extractions) if result else 0}")
        
        # 将结果转换为可序列化的格式
        response_data = {
            'success': True,
            'extractions': [
                {
                    'data': extraction.data,
                    'source_text': extraction.source_text,
                    'chunk_index': extraction.chunk_index,
                    'char_start': extraction.char_start,
                    'char_end': extraction.char_end
                }
                for extraction in result.extractions
            ],
            'metadata': {
                'total_extractions': len(result.extractions),
                'model_used': model_id,
                'chunk_size': chunk_size
            }
        }
        
        return create_response(200, response_data)
    
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {str(e)}")
        return create_response(
            400,
            {'error': 'Invalid JSON format', 'details': str(e)}
        )
    
    except Exception as e:
        print(f"处理请求时发生错误: {str(e)}")
        print(traceback.format_exc())
        return create_response(
            500,
            {'error': 'Internal server error', 'details': str(e)}
        )


def create_response(status_code, body):
    """
    创建标准的 API Gateway 响应
    
    参数:
        status_code (int): HTTP 状态码
        body (dict): 响应体
    
    返回:
        dict: API Gateway 响应格式
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # CORS 支持
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }

