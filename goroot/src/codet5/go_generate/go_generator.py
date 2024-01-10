from transformers import T5ForConditionalGeneration, RobertaTokenizer


class GoGenerator:
    def __init__(self, model_path, device, cache_dir=None):
        self.model = T5ForConditionalGeneration.from_pretrained(model_path, cache_dir=cache_dir).to(device)
        self.tokenizer = RobertaTokenizer.from_pretrained(model_path, cache_dir=cache_dir)
        self.device = device

    def generate(self, input_text):
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids=input_ids, max_new_tokens=256)
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return output_text

    def get_token_num(self, input_text):
        return len(self.tokenizer(input_text, return_tensors="pt").input_ids[0])
