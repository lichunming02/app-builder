# 短文本在线合成（TTS）

## 简介
短文本在线合成组件（TTS）提供高度拟人、流畅自然的语音合成服务，将文本朗读出来，基础音库性价比更高，精品音库听感更逼真。

### 功能介绍
提供高度拟人、流畅自然的语音合成服务

### 特色优势
将文本朗读出来，基础音库性价比更高，精品音库听感更逼真。

### 应用场景
文本朗读


## 基本用法

下面是语音合成的代码示例：
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
tts = appbuilder.TTS()
cwd = os.getcwd()

# 使用baidu-tts模型, 默认返回MP3格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp)
mp3_sample_path = os.path.join(cwd,"sample.mp3")
with open(mp3_sample_path, "wb") as f:
    f.write(out.content["audio_binary"])
print("成功将文本转语音，mp3格式文件已写入：{}".format(mp3_sample_path))

# 使用paddlespeech-tts模型，目前只支持返回WAV格式
wav_sample_path = os.path.join(cwd,"sample.wav")
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
with open(wav_sample_path, "wb") as f:
    f.write(out.content["audio_binary"])
print("成功将文本转语音，wav格式文件已写入：{}".format(wav_sample_path))
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数 （以表格形式展示）
| 参数名称    | 参数类型    | 是否必须 | 描述                                                      | 示例值 |
|---------|---------|------|---------------------------------------------------------|----|
| message   | String  | 是    | 待转成语音的文本                        |    |
| model   | String  | 否    | 默认是`baidu-tts`模型，可选值：`paddlespeech-tts`、`baidu-tts` |    |
| speed | Integer | 否    | 语音语速，默认是5中等语速，取值范围在0~15之间，如果使用paddlespeech-tts模型，参数自动失效 | 10 |
| pitch   | Integer | 否    | 语音音调，默认是5中等音调，取值范围在0~15之间，如果使用paddlespeech-tts模型，参数自动失效 |    |
| volume | Integer | 否    | 语音音量，默认是5中等音量，取值范围在0~15之间，如果使用paddlespeech-tts模型，参数自动失效| 10 |
| person   | Integer | 否    | 语音人物特征，默认是0(度小美),可选值: 1(度小宇) 、0(度小美)、 3(度逍遥-基础)、  4(度丫丫)、 5003(度逍遥-精品)、  5118(度小鹿) 、106(度博文)、 110(度小童)、 111(度小萌)、 103(度米朵)、 5(度小娇), 如果选择模型为paddlespeech-tts，参数自动失效                                                |    |
| audio_type | String  | 否    | 音频文件格式，默认是`mp3`, 如果使用`paddlespeech-tts`模型，参数只能设为`wav`                                                | 10 |
| retry   | Integer | 否    | HTTP重试次数                                                |    |
| timeout | Integer | 否    | HTTP超时时间                                                | 10 |

### 响应参数
| 参数名称     | 参数类型  | 描述  | 示例值 |
|----------|-------|-----|-|
| audio_binary | Bytes | 音频流 | |
### 响应示例
```json
{"audio_binary": ""}
```


### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的文本转语音。


## 更新记录和贡献
* 短文本在线合成 (2024-01)

