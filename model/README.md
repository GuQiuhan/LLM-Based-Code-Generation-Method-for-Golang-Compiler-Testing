---
license: apache-2.0
---

# CodeT5-small-Go_generation
This model is finetuned based on the pre-trained [CodeT5-small model](https://github.com/salesforce/CodeT5#fine-tuning). 
This model is fine-tuned on dataset: [codet5_go-generation](https://huggingface.co/datasets/intm/codet5_go-generation).

> 5.3 upload the initial version.
> 5.6 upload the dataset

The model genarates the missing function body according to the input which privides the necessary class environment and an empty function.

See example below for formatting.
 
# How to use
Here is how to use this model:

```
from transformers import T5ForConditionalGeneration, RobertaTokenizer

# load model and tokenizer
model_path = "intm/codet5-small-go_generation"
tokenizer = RobertaTokenizer.from_pretrained('intm/codet5-small-go_generation')
model = T5ForConditionalGeneration.from_pretrained(model_path)

# use model to generate code 
input_text = "package names\n\nimport \"knative.dev/pkg/kmeta\"\n\n\nfunc Deployment(rev kmeta.Accessor) string {\n\treturn kmeta.ChildName(rev.GetName(), \"-deployment\")\n}\n\n\nfunc ImageCache(rev kmeta.Accessor) string {\n\treturn kmeta.ChildName(rev.GetName(), \"-cache\")\n}\n\n\n\n\nfunc PA(rev kmeta.Accessor) string"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output = model.generate(input_ids=input_ids, max_new_tokens=256)  # max_new_token is same as max_trg_len in dataset

# convert the result to the string
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)


# this prints "return kmeta.ChildName(rev.GetName(), "-pa")"
```

# Training data
YinShicheng

# Training process
GuQiuhan

# Advisor
Prof.WangYu

# Evaluation results
TODO
