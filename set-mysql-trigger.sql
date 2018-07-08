DROP trigger IF EXISTS face_eye.face_characteristic_to_redis;

DELIMITER $$
CREATE TRIGGER create_trigger AFTER
CREATE TRIGGER face_characteristic_to_redis AFTER INSERT ON face_eye.face_recognizing_facecharacteristic
FOR EACH ROW
BEGIN
SET @ret1=redis_servers_set_v2("redis", 6379);
SET @ret2=redis_command_v2("set", concat(":1:unique_id:", NEW.unique_id), NEW.characteristic_value);
END$$
DELIMITER ;