# LLM-Based Code Generation Method for Golang Compiler Testing
***

## Update:

🎉🎉This paper was published in ESEC/FSE Conference in December, 2023. It also won me the Student Research Competition (Undergraduate Division) at the conference held from December 3 to7, 2023, in San Francisco.

***

This is the official PyTorch implementation for our paper:

**Title**: LLM-Based Code Generation Method for Golang Compiler Testing [[PDF]](https://guqiuhan.github.io/publication/conference-paper/conference-paper.pdf)

**Authors**: [Qiuhan Gu](https://guqiuhan.github.io/), Shicheng Yin and [Yu Wang](https://itwoi.github.io)

![v5.drawio 8.crswap.drawio (5)_00](images/v5.drawio%208.crswap.drawio%20(5)_00.png)

***

# Table of Contents

1. [Introduction](#Introduction)

2. [Model](#Model)
3. [Dataset](#Dataset)
4. [Acknowledgments](#Acknowledgments)

# Introduction

This repo provides the code for reproducing the experiments in **LLM-Based Code Generation Method for Golang Compiler Testing**. We present a LLM-based high-quality code generation method and implement it on Golang compiler testing. To summarize, our contributions in this work include:

* A LLM-based high-quality code generation method.
* Apply the method to the Golang compiler, generating testcases with 3.38% average coverage. It detects only 2.79% of syntax errors and 0% of undefined behavior in the testcases.

### How to reproduce the result?

Go to `scripts/goroot/src/codet5` folder, you can use `./script.sh` to reproduce the experiment.

# Model

Our model is finetuned based on the pre-trained [CodeT5-small model](https://github.com/salesforce/CodeT5#fine-tuning). Our model can genarate the missing function body according to the input which privides the necessary class environment and an empty function. You can find them in `model` folder or in [huggingface web](https://huggingface.co/intm/codet5-small-go_generation).

See example below for formatting.

## How to use

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

# Dataset

We process and filter Go language code files from the internet with the help of the syntax analysis tool tree-sitter [18] to obtain Go language code files that meet our requirements. Thus, we prepare the filtered dataset, which contains 1839 pieces of program, for model training and initial seed choice. You can find them in `dataset` folder or in [huggingface web](https://huggingface.co/datasets/intm/codet5_go-generation/tree/main).

# Acknowledgments
This work was supported by the National Natural Science Foundation of China under Grant No. 62232001 and No. 62202220