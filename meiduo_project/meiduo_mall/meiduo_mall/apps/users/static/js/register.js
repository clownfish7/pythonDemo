// 创建 Vue 对象
let app = new Vue({
    // 通过 ID 选择器找到绑定 HTML 的内容
    el: '#app',
    // 数据绑定对象
    data: {
        // v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',

        // v-show
        error_username: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,

        // error_message
        error_username_message: '',
        error_mobile_message: '',
    },
    methods: {
        // 定义和实现事件方法

        // 校验用户名
        check_username: () => {

        },
        // 校验密码
        check_password: () => {

        },
        // 校验确认密码
        check_password2: () => {

        },
        // 校验手机号
        check_mobile: () => {

        },
        // 校验是否勾选协议
        check_allow: () => {

        },
        // 监听表单提交事件
        on_submit: () => {

        },
    }
})