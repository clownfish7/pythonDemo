// 创建 Vue 对象
let app = new Vue({
    // 通过 ID 选择器找到绑定 HTML 的内容
    el: '#app',
    delimiters: ['[[', ']]'],
    // 数据绑定对象
    data: {
        // v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        image_code: '',
        sms_send_flag: false,

        // v-show
        error_username: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

        // error_message
        error_username_message: '',
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: '',

        image_code_url: '',
        uuid: '',
        sms_code_tip: '获取短信验证码',
    },
    mounted() {
        // 页面加载完调用
        this.generate_image_code()
    },
    methods: {
        // 定义和实现事件方法

        // 生成图形验证码
        generate_image_code() {
            this.uuid = generateUUID()
            this.image_code_url = 'verifications/image_codes/' + this.uuid + '/'
        },

        // 短信验证
        send_sms_code() {
            if (this.sms_send_flag) {
                return
            }
            this.check_image_code()
            this.check_mobile()
            if (this.error_mobile || this.error_image_code) {
                return;
            }
            this.sms_send_flag = true
            let url = 'verifications/sms_codes/' + this.mobile
                + '?image_code=' + this.image_code
                + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(resp => {
                    if (resp.data.code === '0') {
                        let num = 60
                        let interval = setInterval(() => {
                            if (num === 1) {
                                clearInterval(interval)
                                this.sms_code_tip = '获取短信验证码'
                                this.generate_image_code()
                                this.sms_send_flag = false
                            }
                            num -= 1;
                            this.sms_code_tip = num + 's'
                        }, 1000);
                    } else {
                        this.sms_code_tip = resp.data.message
                        this.sms_send_flag = false
                    }
                })
                .catch(error => {
                    console.error(error.response)
                    this.sms_send_flag = false
                })
        },

        // 校验用户名
        check_username: function () {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username_message = '请输入5-20个字符的用户名';
                this.error_username = true;
            }
            if (!this.error_username) {
                let url = '/users/' + this.username + '/count/'
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.data.count === 1) {
                            // username exists
                            this.error_username = true
                            this.error_username_message = '用户名已存在'
                        } else {
                            // username not exists
                            this.error_username = false
                        }
                    })
                    .catch(error => {
                        console.error(error.response)
                    })
            }
        },
        // 校验密码
        check_password: function () {
            let re = /^[0-9A-Za-z]{8,20}$/;
            this.error_password = !re.test(this.password);
        },
        // 校验确认密码
        check_password2: function () {
            this.error_password2 = this.password !== this.password2;
        },
        // 校验手机号
        check_mobile: function () {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },
        // 校验图形验证码
        check_image_code: function () {
            if (this.image_code.length !== 4) {
                this.error_image_code_message = '请输入图形验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },
        // 校验是否勾选协议
        check_allow: function () {
            this.error_allow = !this.allow;
        },
        check_sms_code() {
            if (this.sms_code.length !== 6) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },
        // 监听表单提交事件
        on_submit: function () {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            this.check_sms_code();
            if (this.error_username === true ||
                this.error_password === true ||
                this.error_password2 === true ||
                this.error_mobile === true ||
                this.error_allow === true ||
                this.error_sms_code === true) {
                // 禁用表单的提交
                window.event.returnValue = false;
            }
        }
    }
})