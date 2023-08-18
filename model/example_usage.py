

from transformers import T5ForConditionalGeneration, RobertaTokenizer

# 加载模型和tokenizer
model_path = "intm/codet5-small-go_generation"
tokenizer = RobertaTokenizer.from_pretrained('intm/codet5-small-go_generation')
model = T5ForConditionalGeneration.from_pretrained(model_path)

# 使用模型进行推理
input_text = "package names\n\nimport \"knative.dev/pkg/kmeta\"\n\n\nfunc Deployment(rev kmeta.Accessor) string {\n\treturn kmeta.ChildName(rev.GetName(), \"-deployment\")\n}\n\n\nfunc ImageCache(rev kmeta.Accessor) string {\n\treturn kmeta.ChildName(rev.GetName(), \"-cache\")\n}\n\n\n\n\nfunc PA(rev kmeta.Accessor) string"
#input_text="\n\nfunc twoSum(nums []int, target int) []int "
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output = model.generate(input_ids=input_ids, max_new_tokens=256)  #最大长度按照数据集的max_trg_len设置

# 将生成的结果转换为字符串
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)


# 应当可以输出：return rev.GetName()
