[![Build Status](https://cloud.drone.io/api/badges/samcre/drone-slack-file/status.svg?ref=refs/heads/master)](https://cloud.drone.io/samcre/drone-slack-file)

# drone-slack-file

Drone plugin to send pipeline's files to Slack webhook.

## Usage

```yaml
steps:
  - name: send_file_to_slack
    image: samcre/drone-slack-file
    settings:
      file: path_to/your_file.txt
      webhook:
        from_secret: SLACK_WEBHOOK
      drone_server: https://drone.example.com
```

## Settings

You can use this settings as environment variables prepending with `PLUGIN_$settingName`, e.g.: `PLUGIN_WEBHOOK`:

* `file`: Path to the file you want to send to Slack.
* `webhook`: URL of the Slack webhook.
* `drone_server`: _optional_ URL of your Drone server.

## Limitations

As you may know, Slack have a limitation of characters when sending messages. Currently, it's 3000 characters per block. If your file contains more than 3000 characters, it's truncated to send only latest 3000, and send another message with a URL to your Drone build, if you provided the `drone_server` setting.

## Workaround for file permissions on Drone pipelines

If you are using Drone Docker pipelines, there can be some issues with file permissions at creation time. To solve that, add this step to your pipeline:

```yaml
  - name: create_output_file
    image: alpine
    commands:
      - touch output.log
      - chmod 777 output.log
  # After this, you can write the file with an image using UID != 0

  - name: your_process
    image: your_image:latest
    commands:
      - python /usr/src/app/your_app.py 2>&1 | tee -a output.log

  - name: sned_file_to_slack
    image: samcre/drone-slack-file
    settings:
      file: output.log
      webhook:
        from_secret: SLACK_WEBHOOK
      drone_server: https://drone.example.com
```
