# FaceRecognition & EyeTracking

### 说明
本项目是一个根据所给图片进行人脸识别和眼球运动方向追踪的后台应用.

### APIs
#### 眼球方向识别
api: `/eye-tracking/get-eyeball-direction`

方法: `POST`

参数: 
	`face_image`, 格式: `form-data`, 文件: 人脸图片

结果:
1. 识别成功, 返回{"result": direction}, "direction"为识别的眼球方向
2. 未检测到图中人脸, 返回{"result": "can not detect faces"};
3. 图片存储失败, 返回{"result": "image store error"}, 原因可能为图片过大或网络问题;

##### 眼球方向识别功能已单独抽象成python模块发布到pypi, 可直接进行复用, 详情👉[见此项目](https://github.com/VanjayDo/eye_game)

#### 脸部识别
api: `/face-recognizing/recognize-face`

方法: `POST`

参数(`form-data`格式): 
	 `face_image` , 类型: file(人脸图片)
	 `unique_id`,  类型: text(用户id)

结果:
1. 识别成功, 返回{"result": True, "user-id": True/False}, "user-id"为数据库中保存的用户身份id;
2. 未识别出, 返回{"result": False, "add": True/False}, "add"为该脸部信息在此次识别过程中成功是否添加进数据库, 未识别出来且添加失败则是user-id已被使用(user-id要保证唯一);
3. 未检测到图中人脸, 返回{"result": "can not detect faces"};
4. 图片存储失败, 返回{"result": "image store error"}, 原因可能为图片过大或网络问题;

### 文件说明
`requirements.txt`: pip导出的项目依赖;

`set-mysql-trigger.sql`: 创建mysql数据库中自动更新新插入数据到redis缓存的trigger;

`Dockerfile`: 构建face-eye容器的dockerfile;

`docker-compose.yml`: 编排整个项目的compose配置文件;

`docker-mysql2redis/`: 存放定制mysql2redis镜像的dockerfile;