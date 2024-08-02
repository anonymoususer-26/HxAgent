from error import InvalidOpenAIFinishReasonError, FailedOpenAIRequestError
from openai import OpenAI
from config import GLOBAL_CONFIG
import json

class APIUsageManager:
    usage = {}
    response_time = {}

    @classmethod
    def record_usage(cls, module, model, usage):
        if module not in cls.usage:
            cls.usage[module] = {
                'model': model,
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0,
            }
        cls.usage[module]['prompt_tokens'] += usage.prompt_tokens
        cls.usage[module]['completion_tokens'] += usage.completion_tokens
        cls.usage[module]['total_tokens'] += usage.total_tokens

    @classmethod
    def record_response_time(cls, model, response_time):
        if model not in cls.response_time:
            cls.response_time[model] = []
        cls.response_time[model].append(response_time)

    @classmethod
    def get_usage(cls):
        return cls.usage
    
    @classmethod
    def get_response_time(cls):
        return cls.response_time
    
    @classmethod
    def reset(cls):
        cls.usage = {}
        cls.response_time = {}

class Agent:
  def ask(prompt, model=None, temperature = 0, module = "all", json_response=True):
    client = OpenAI(api_key = GLOBAL_CONFIG['agent']['key'])
    model = model if model else GLOBAL_CONFIG['agent']['model']
    response = None
    try:
      if json_response:
        response = client.chat.completions.create(
          model= model,
          messages=prompt,
          temperature=temperature,
          response_format={ 'type': 'json_object' },
          seed=0
        )
      else:
        response = client.chat.completions.create(
          model= model,
          messages=prompt,
          temperature=temperature,
          seed=0
        )
    except Exception as e:
      raise FailedOpenAIRequestError(e)
    
    if (response.choices[0].finish_reason != "stop"):
      raise InvalidOpenAIFinishReasonError()
    
    APIUsageManager.record_usage(module, model, response.usage)
    if (json_response):
      return json.loads(response.choices[0].message.content)
    else:
      return response.choices[0].message.content