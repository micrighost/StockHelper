<template>
  <div id="app">
    <div class="wrapper">
        <!-- Sidebar  -->
        <nav id="sidebar" :class="{active: sidebar_Status}">
          <!-- User Info-->
          <div class="sidenav-header-inner text-center">
              <img src="@/assets/anonymous.jpg" alt="user_image"  class="img-fluid rounded-circle user_image" v-if="user_image_url === ''">
              <img :src="user_image_url" alt="user_image"  class="img-fluid rounded-circle user_image" v-else>
              <h6 class="#homeSubmenu" aria-expanded="false">{{ username }}</h6>
              <label class="switch">
                  <input type="checkbox" checked class="btn btn-info" @click="toggle_sidebar()">
                  <span class="slider round"></span>
              </label>
          </div>
            <ul class="list-unstyled components">
                <li>
                  <a href="#userinfo" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                      <i class="fas fa-copy"></i>
                      個人資訊
                  </a>
                  <ul class="collapse list-unstyled" id="userinfo">
                      <li>
                        <router-link :to="{ name: 'UserInfo'}">持有庫存</router-link>
                      </li>
                  </ul>
                </li>
                <li>
                  <a href="#stockinfo" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                      <i class="fas fa-home"></i>
                      股票資訊
                  </a>
                  <ul class="collapse list-unstyled" id="stockinfo">
                      <li>
                        <router-link :to="{ name: 'StockData'}">個股資訊</router-link>
                      </li>
                  </ul>
                </li>
                <li>
                  <a href="#pageSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                      <i class="fas fa-copy"></i>
                      智能預測
                  </a>
                  <ul class="collapse list-unstyled" id="pageSubmenu">
                      <li>
                        <router-link :to="{ name: 'AI_Predict'}">價格預測</router-link>
                      </li>
                  </ul>
                </li>
            </ul>
        </nav>

        <!-- Page Content  -->
        <div id="content">
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <img class="stock_increase_image" src="@/assets/stock_increase.png" alt="stock_increase">
                    <a href="http://www.stockhelper.com.tw:8080/">
                        <h2 class="text-center red_text">StockHelper</h2>
                    </a>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="nav navbar-nav ml-auto">
                            <li class="nav-item active">
                                <router-link class="nav-link" to="" data-toggle="modal" data-target="#exampleModal">LogOut</router-link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <router-view/>
        </div>
    </div>
    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
                確定要登出嗎?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="sign_out()">Yes</button>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'App',
    data: function () {
        return {
          sidebar_Status: false,
          username: this.$store.getters.username,
          user_image_url: this.$store.getters.user_image_url,
        }
    },
    created: function () {
      this.get_user_info()
    },
    mounted: function () {

    },
    methods: {
        toggle_sidebar: function () {
          this.sidebar_Status = !this.sidebar_Status
        },
        sign_out: function () {
            gapi.auth2.init()
            gapi.auth2.getAuthInstance()
            var auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut()
            // 轉頁
            this.delete_cookie('google_token')
            location.href = 'http://www.stockhelper.com.tw:8080/login'
        },
        delete_cookie:  function(name) {
            document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        },
        get_cookie: function (name) {
            var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
            if (match) return match[2];
        },
        get_user_info: function() {
          // Connect API
          if (this.$router.currentRoute.name === 'Login') {
            return true
          }
          const google_token = this.get_cookie('google_token')
          const parent_this = this
          const vuex_store = this.$store
          axios({
              method: 'get',
              url: 'http://www.stockhelper.com.tw:8889/api/users',
              params: { 'google_token': google_token}
          })
          .then(function (response) {
              vuex_store.dispatch('update_user_info', response.data)
              parent_this.username = vuex_store.getters.username
              parent_this.user_image_url = vuex_store.getters.user_image_url
          })
          .catch(function (error) {
            // console.log(error);
            parent_this.delete_cookie('google_token')
            alert('請登入。')
            parent_this.$router.push({ name: 'Login'})
          })
        }
    }
}
</script>

<style>
  /* custom CSS */
  @import "assets/index/css/index.css";
  /* Bootstrap CSS */
  @import "https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css";
  /* Font Awesome JS */
  @import "https://use.fontawesome.com/releases/v5.0.13/js/solid.js";
  @import "https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js";
</style>
