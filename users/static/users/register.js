if (parent.callback) {
    //如果是在子框架内就把首页刷新
    parent.callback();
}
var registerApp = new Vue({
        el: '.login-main',
        data: {
            username: '',
            password: '',
            password2: '',
            last_name: '',
            first_name: '',
            loading: false
        },
        methods: {
            createUser: function () {
                this.loading = true;
                if (this.username === "") {
                    this.$message.error("请输入用户名！");
                    this.loading = false;
                    return;
                } else {
                    const reg = /^([a-zA-Z0-9]+[-_\.]?)+@[a-zA-Z0-9]+\.[a-z]+$/;
                    if (!reg.test(this.username)) {
                        this.$message.error("用户名不是合法的邮箱地址！");
                        this.loading = false;
                        return;
                    }
                }
                if (this.password === "") {
                    this.$message.error("请输入密码！");
                    this.loading = false;
                    return;
                }
                if (this.password2 === "") {
                    this.$message.error("请进行密码确认！");
                    this.loading = false;
                    return;
                }
                if (this.password !== this.password2) {
                    this.$message.error("密码不一致！");
                    this.loading = false;
                    return;
                }
                if (this.last_name === "" || this.first_name === "") {
                    this.$message.error("请输入姓名！");
                    this.loading = false;
                    return;
                }

                this.$nextTick(function () {
                    document.getElementById('login-form').submit();
                });
            }
        }
    })
;

