# Text_to_Json 将文本文件制作为json文件

## 制作文本文件
  *文本文件的制作我们通过‘|’进行区分，分为语料部分，问题部分以及答案部分，其中答案之间以‘;’进行区分
  **制作的文本文件以utf-8进行编码
  **新制作的文本文件行首有一个小圆点，应该去掉
  
 ## 运行augment_data.py
  *运行上面的代码，制作相应的json文件
  
 ## 运行Multi_Span_To_Json.py文件
  *运行上面的代码，制作训练以及预测json文件
  **这一过程首先制作csv文件，再之后将csv文件转换为json文件
