<div align="center">

<h1>Image Embed | Worker</h1>

</div>

## Model Inputs

| Input                               | Type  | Description                                                                                                             |
|-------------------------------------|-------|-------------------------------------------------------------------------------------------------------------------------|
| `image`                             | Path  | Image file                                                                                                              |
| `image_base64`                      | str   | Base64-encoded image file                                                                                               |
| `model`                             | str   | Choose a Whisper model. Choices: "tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3". Default: "base" |

## Test Inputs

The following inputs can be used for testing the model:

```json
{
    "input": {
        "audio": "https://github.com/runpod-workers/sample-inputs/blob/main/images/Utah_teapot.png"
    }
}
```

## Sample output

```json
{
  "result": []
}
```
