from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    @abstractmethod
    def process(self, obj):
        pass

class DuanshuStrategy(ProcessingStrategy):
    def process(self, obj):
        print("使用 duanshu 策略处理对象:", obj)
        # 具体实现

class XiangshuStrategy(ProcessingStrategy):
    def process(self, obj):
        print("使用 xiangshu 策略处理对象:", obj)
        # 具体实现

class Processor:
    def __init__(self):
        self.strategies = {
            "duanshu": DuanshuStrategy(),
            "xiangshu": XiangshuStrategy()
        }
    
    def process(self, strategy_name, obj):
        strategy = self.strategies.get(strategy_name)
        if strategy:
            strategy.process(obj)
        else:
            raise ValueError(f"未知的策略: {strategy_name}")

# 使用示例
processor = Processor()
processor.process("duanshu", {"data": 123})
processor.process("xiangshu", {"data": 456})