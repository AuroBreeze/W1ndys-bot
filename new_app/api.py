# handlers/api.py

import json
import logging


# 发送私聊消息
async def send_private_msg(websocket, user_id, content):
    message = {
        "action": "send_private_msg",
        "params": {"user_id": user_id, "message": content},
    }
    await websocket.send(json.dumps(message))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已发送消息到用户 {user_id}: {content}")
    else:
        logging.error(f"发送消息到用户 {user_id} 失败: {response_data}")


# 发送群消息
async def send_group_msg(websocket, group_id, content):
    message = {
        "action": "send_group_msg",
        "params": {"group_id": group_id, "message": content},
    }
    await websocket.send(json.dumps(message))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已发送消息到群 {group_id}: {content}")
    else:
        logging.error(f"发送消息到群 {group_id} 失败: {response_data}")


# 发送消息
async def send_msg(websocket, message_type, user_id, group_id, message):
    message = {
        "action": "send_msg",
        "params": {
            "message_type": message_type,
            "user_id": user_id,
            "group_id": group_id,
            "message": message,
        },
    }
    await websocket.send(json.dumps(message))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已发送消息: {message}")
    else:
        logging.error(f"发送消息失败: {response_data}")


# 撤回消息
async def delete_msg(websocket, message_id):
    delete_msg = {
        "action": "delete_msg",
        "params": {"message_id": message_id},
    }
    await websocket.send(json.dumps(delete_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"消息 {message_id} 已撤回。")
    else:
        logging.error(f"撤回消息 {message_id} 失败: {response_data}")


# 获取消息
async def get_msg(websocket, message_id):
    get_msg = {
        "action": "get_msg",
        "params": {"message_id": message_id},
    }
    await websocket.send(json.dumps(get_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取消息 {message_id}。")
    else:
        logging.error(f"获取消息 {message_id} 失败: {response_data}")


# 获取合并转发消息
async def get_forward_msg(websocket, id):
    get_forward_msg = {
        "action": "get_forward_msg",
        "params": {"message_id": id},
    }
    await websocket.send(json.dumps(get_forward_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取合并转发消息 {id}。")
    else:
        logging.error(f"获取合并转发消息 {id} 失败: {response_data}")


# 发送好友赞
async def send_like(websocket, user_id, times):
    like_msg = {
        "action": "send_like",
        "params": {"user_id": user_id, "times": times},
    }
    await websocket.send(json.dumps(like_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已发送好友赞 {user_id} {times} 次。")
    else:
        logging.error(f"发送好友赞 {user_id} 失败: {response_data}")


# 群组踢人
async def set_group_kick(websocket, group_id, user_id):
    kick_msg = {
        "action": "set_group_kick",
        "params": {"group_id": group_id, "user_id": user_id},
    }
    await websocket.send(json.dumps(kick_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已踢出用户 {user_id}。")
        await send_group_msg(websocket, group_id, f"已踢出用户 {user_id}。")
    else:
        logging.error(f"踢出用户 {user_id} 失败: {response_data}")


# 群组单人禁言
async def set_group_ban(websocket, group_id, user_id, duration):
    ban_msg = {
        "action": "set_group_ban",
        "params": {"group_id": group_id, "user_id": user_id, "duration": duration},
    }
    await websocket.send(json.dumps(ban_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已禁止用户 {user_id} {duration} 秒。")
    else:
        logging.error(f"禁止用户 {user_id} 失败: {response_data}")


# 群组匿名用户禁言
async def set_group_anonymous_ban(websocket, group_id, anonymous_flag, duration):
    anonymous_ban_msg = {
        "action": "set_group_anonymous_ban",
        "params": {"group_id": group_id, "flag": anonymous_flag, "duration": duration},
    }
    await websocket.send(json.dumps(anonymous_ban_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已禁止匿名用户 {anonymous_flag} {duration} 秒。")
    else:
        logging.error(f"禁止匿名用户 {anonymous_flag} 失败: {response_data}")


# 群组全员禁言
async def set_group_whole_ban(websocket, group_id, enable):
    whole_ban_msg = {
        "action": "set_group_whole_ban",
        "params": {"group_id": group_id, "enable": enable},
    }
    await websocket.send(json.dumps(whole_ban_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        await send_group_msg(
            websocket,
            group_id,
            f"已{'开启' if enable else '解除'}群 {group_id} 的全员禁言。",
        )
        logging.info(f"已{'开启' if enable else '解除'}群 {group_id} 的全员禁言。")
    else:
        logging.error(
            f"群 {group_id} 的全员禁言 {'开启' if enable else '解除'}失败: {response_data}"
        )


# 群组设置管理员
async def set_group_admin(websocket, group_id, user_id, enable):
    admin_msg = {
        "action": "set_group_admin",
        "params": {"group_id": group_id, "user_id": user_id, "enable": enable},
    }
    await websocket.send(json.dumps(admin_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(
            f"已{'授予' if enable else '解除'}群 {group_id} 的管理员 {user_id} 的权限。"
        )
    else:
        logging.error(f"设置管理员 {user_id} 失败: {response_data}")


# 群组匿名
async def set_group_anonymous(websocket, group_id, enable):
    anonymous_msg = {
        "action": "set_group_anonymous",
        "params": {"group_id": group_id, "enable": enable},
    }
    await websocket.send(json.dumps(anonymous_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已{'开启' if enable else '关闭'}群 {group_id} 的匿名。")
    else:
        logging.error(f"设置群 {group_id} 的匿名失败: {response_data}")


# 设置群名片（群备注）
async def set_group_card(websocket, group_id, user_id, card):
    card_msg = {
        "action": "set_group_card",
        "params": {"group_id": group_id, "user_id": user_id, "card": card},
    }
    await websocket.send(json.dumps(card_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已设置群 {group_id} 的用户 {user_id} 的群名片为 {card}。")
    else:
        logging.error(f"设置群名片 {card} 失败: {response_data}")


# 设置群名
async def set_group_name(websocket, group_id, group_name):
    name_msg = {
        "action": "set_group_name",
        "params": {"group_id": group_id, "group_name": group_name},
    }
    await websocket.send(json.dumps(name_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已设置群 {group_id} 的群名为 {group_name}。")
    else:
        logging.error(f"设置群名 {group_name} 失败: {response_data}")


# 退出群组
async def set_group_leave(websocket, group_id, is_dismiss):
    leave_msg = {
        "action": "set_group_leave",
        "params": {"group_id": group_id, "is_dismiss": is_dismiss},
    }
    await websocket.send(json.dumps(leave_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已退出群 {group_id}。")
    else:
        logging.error(f"退出群 {group_id} 失败: {response_data}")


# 设置群组专属头衔
async def set_group_special_title(
    websocket, group_id, user_id, special_title, duration
):
    special_title_msg = {
        "action": "set_group_special_title",
        "params": {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration,
        },
    }
    await websocket.send(json.dumps(special_title_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(
            f"已设置群 {group_id} 的用户 {user_id} 的专属头衔为 {special_title}。"
        )
    else:
        logging.error(f"设置专属头衔 {special_title} 失败: {response_data}")


# 处理加好友请求
async def set_friend_add_request(websocket, flag, approve):
    request_msg = {
        "action": "set_friend_add_request",
        "params": {"flag": flag, "approve": approve},
    }
    await websocket.send(json.dumps(request_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已{'同意' if approve else '拒绝'}好友请求。")
    else:
        logging.error(f"处理好友请求失败: {response_data}")


# 处理加群请求／邀请
async def set_group_add_request(websocket, flag, type, approve, reason):
    request_msg = {
        "action": "set_group_add_request",
        "params": {"flag": flag, "type": type, "approve": approve, "reason": reason},
    }
    await websocket.send(json.dumps(request_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已{'同意' if approve else '拒绝'}群 {type} 请求。")
    else:
        logging.error(f"处理群 {type} 请求失败: {response_data}")


# 获取登录号信息
async def get_login_info(websocket):
    login_info_msg = {
        "action": "get_login_info",
        "params": {},
    }
    await websocket.send(json.dumps(login_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取登录号信息。")
    else:
        logging.error(f"获取登录号信息失败: {response_data}")


# 获取陌生人信息
async def get_stranger_info(websocket, user_id, no_cache=False):
    stranger_info_msg = {
        "action": "get_stranger_info",
        "params": {"user_id": user_id, "no_cache": no_cache},
    }
    await websocket.send(json.dumps(stranger_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取陌生人 {user_id} 信息。")
    else:
        logging.error(f"获取陌生人 {user_id} 信息失败: {response_data}")


# 获取好友列表
async def get_friend_list(websocket):
    friend_list_msg = {
        "action": "get_friend_list",
        "params": {},
    }
    await websocket.send(json.dumps(friend_list_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取好友列表。")
    else:
        logging.error(f"获取好友列表失败: {response_data}")


# 获取群信息
async def get_group_info(websocket, group_id):
    group_info_msg = {
        "action": "get_group_info",
        "params": {"group_id": group_id},
    }
    await websocket.send(json.dumps(group_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取群 {group_id} 信息。")
    else:
        logging.error(f"获取群 {group_id} 信息失败: {response_data}")


# 获取群列表
async def get_group_list(websocket):
    group_list_msg = {
        "action": "get_group_list",
        "params": {},
    }
    await websocket.send(json.dumps(group_list_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取群列表。")
    else:
        logging.error(f"获取群列表失败: {response_data}")


# 获取群成员信息
async def get_group_member_info(websocket, group_id, user_id, no_cache=False):
    group_member_info_msg = {
        "action": "get_group_member_info",
        "params": {"group_id": group_id, "user_id": user_id, "no_cache": no_cache},
    }
    await websocket.send(json.dumps(group_member_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取群 {group_id} 的成员 {user_id} 信息。")
    else:
        logging.error(f"获取群成员 {user_id} 信息失败: {response_data}")


# 获取群成员列表
async def get_group_member_list(websocket, group_id):
    group_member_list_msg = {
        "action": "get_group_member_list",
        "params": {"group_id": group_id},
    }
    await websocket.send(json.dumps(group_member_list_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取群 {group_id} 的成员列表。")
    else:
        logging.error(f"获取群 {group_id} 的成员列表失败: {response_data}")


# 获取群荣誉信息
async def get_group_honor_info(websocket, group_id, type):
    honor_info_msg = {
        "action": "get_group_honor_info",
        "params": {"group_id": group_id, "type": type},
    }
    await websocket.send(json.dumps(honor_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取群 {group_id} 的 {type} 荣誉信息。")
    else:
        logging.error(f"获取群 {group_id} 的 {type} 荣誉信息失败: {response_data}")


# 获取 Cookies
async def get_cookies(websocket):
    cookies_msg = {
        "action": "get_cookies",
        "params": {},
    }
    await websocket.send(json.dumps(cookies_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取 Cookies。")
    else:
        logging.error(f"获取 Cookies 失败: {response_data}")


# 获取 CSRF Token
async def get_csrf_token(websocket):
    csrf_token_msg = {
        "action": "get_csrf_token",
        "params": {},
    }
    await websocket.send(json.dumps(csrf_token_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取 CSRF Token。")
    else:
        logging.error(f"获取 CSRF Token 失败: {response_data}")


# 获取 QQ 相关接口凭证
async def get_credentials(websocket):
    credentials_msg = {
        "action": "get_credentials",
        "params": {},
    }
    await websocket.send(json.dumps(credentials_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取 QQ 相关接口凭证。")
    else:
        logging.error(f"获取 QQ 相关接口凭证失败: {response_data}")


# 获取语音
async def get_record(websocket, file, out_format, full_path):
    record_msg = {
        "action": "get_record",
        "params": {"file": file, "out_format": out_format, "full_path": full_path},
    }
    await websocket.send(json.dumps(record_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取语音 {file}。")
    else:
        logging.error(f"获取语音 {file} 失败: {response_data}")


# 获取图片
async def get_image(websocket, file, out_format, full_path):
    image_msg = {
        "action": "get_image",
        "params": {"file": file, "out_format": out_format, "full_path": full_path},
    }
    await websocket.send(json.dumps(image_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已获取图片 {file}。")
    else:
        logging.error(f"获取图片 {file} 失败: {response_data}")


# 检查是否可以发送图片
async def can_send_image(websocket):
    can_send_image_msg = {
        "action": "can_send_image",
        "params": {},
    }
    await websocket.send(json.dumps(can_send_image_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已检查是否可以发送图片。")
    else:
        logging.error(f"检查是否可以发送图片失败: {response_data}")


# 检查是否可以发送语音
async def can_send_record(websocket):
    can_send_record_msg = {
        "action": "can_send_record",
        "params": {},
    }
    await websocket.send(json.dumps(can_send_record_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已检查是否可以发送语音。")
    else:
        logging.error(f"检查是否可以发送语音失败: {response_data}")


# 获取运行状态
async def get_status(websocket):
    status_msg = {
        "action": "get_status",
        "params": {},
    }
    await websocket.send(json.dumps(status_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取运行状态。")
    else:
        logging.error(f"获取运行状态失败: {response_data}")


# 获取版本信息
async def get_version_info(websocket):
    version_info_msg = {
        "action": "get_version_info",
        "params": {},
    }
    await websocket.send(json.dumps(version_info_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已获取版本信息。")
    else:
        logging.error(f"获取版本信息失败: {response_data}")


# 重启 OneBot 实现
async def set_restart(websocket, delay=0):
    restart_onebot_msg = {
        "action": "set_restart",
        "params": {"delay": delay},
    }
    await websocket.send(json.dumps(restart_onebot_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已重启 OneBot 实现。")
    else:
        logging.error(f"重启 OneBot 实现失败: {response_data}")


# 清理缓存
async def clean_cache(websocket):
    clean_cache_msg = {
        "action": "clean_cache",
        "params": {},
    }
    await websocket.send(json.dumps(clean_cache_msg))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info("已清理缓存。")
    else:
        logging.error(f"清理缓存失败: {response_data}")


# 解析并执行命令
async def execute_command(websocket, action, params):
    try:
        params_json = json.loads(params)

        if not action:
            logging.error("无效的命令: 缺少 action")
            return

        logging.info(f"即将执行API命令: {action} {params_json}")
        await run_api(websocket, action, params_json)
    except json.JSONDecodeError:
        logging.error("参数解析失败: 无效的 JSON 格式")
    except Exception as e:
        logging.error(f"执行命令时出错: {e}")


# 执行API调用
async def run_api(websocket, action, params):
    api_message = {"action": action, "params": params}
    await websocket.send(json.dumps(api_message))
    response = await websocket.recv()
    response_data = json.loads(response)
    if response_data.get("status") == "ok":
        logging.info(f"已调用 API {action}。")
    else:
        logging.error(f"调用 API {action} 失败: {response_data}")