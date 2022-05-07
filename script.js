const LoginPage = {
  template:`
 <div class='container'>
  <div class="wrapper">
      <div class="logo">
          <img src="https://www.freepnglogos.com/uploads/wheat-png/wheat-premium-agriculture-icons-canva-34.png" alt="">
      </div>
      <div class="text-center mt-4 name">
          <strong>Irrigation Managment App</strong>
      </div>
      <form class="p-3 mt-3">
          <div class="form-field d-flex align-items-center">
              <span class="far fa-user"></span>
              <input type="text" name="userName" id="userName" placeholder="Phone number">
          </div>
          <div class="form-field d-flex align-items-center">
              <span class="fas fa-key"></span>
              <input type="password" name="password" id="pwd" placeholder="Password">
          </div>
          <button class="btn mt-3">Login</button>
      </form>
      <div class="text-center fs-6">
          <a href="#">Forget password?</a> or <a href="file:///C:/Users/Himasnhu%20pratap/Desktop/Irrigation%20Managment%20App/index.html#/signup">Sign up</a>
      </div>
  </div>
  </div>
  `,
  data: function(){
    return{
      email: undefined,
      password : undefined
    }
  },
  methods:{
    login: async function(){
      if (this.email === undefined || this.password === undefined){
        alert("Fields cannot be empty");
      }
      else{
        const res = await fetch('HTTP://127.0.0.1:5000/loginapi',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"email":this.email,"password":this.password})
    });
    //console.log(res,"sjjjjjjjjjjjjjj",res.json());
    if (res.status == 200){
      let data = await res.json()
      if (data != null){
        localStorage.setItem('token', data["token"])
        this.$router.push('/dashboard')
      }
    }
    else{
      alert('Incorrect username or password, please sign up if you have not signed up');
    }
  }
      },
    reverse: function(){
      this.message = this.message.split('').reverse().join('')
    }
  }

}
const SignUp = {
  template:`
 <div class='container'>
  <div class="wrapper">
      <div class="logo">
          <img src="https://www.freepnglogos.com/uploads/wheat-png/wheat-premium-agriculture-icons-canva-34.png" alt="">
      </div>
      <div class="text-center mt-4 name">
          <strong>Irrigation Managment App</strong>
      </div>
      <form class="p-3 mt-3">
          <div class="form-field d-flex align-items-center">
              <span class="far fa-user"></span>
              <input type="text" name="userName" id="userName" placeholder="Username">
          </div>
          <div class="form-field d-flex align-items-center">
              <span class="far fa-user"></span>
              <input type="text" name="userName" id="userName" placeholder="Phone number">
          </div>
          <div class="form-field d-flex align-items-center">
              <span class="fas fa-key"></span>
              <input type="password" name="password" id="pwd" placeholder="Password">
          </div>
          <button class="btn mt-3">Signup</button>
      </form>
      <div class="text-center fs-6">
          Have an account <a href="#">login!</a>
      </div>
  </div>
  </div>
  `,
  data: function(){
    return{
      email: undefined,
      password : undefined
    }
  },
  methods:{
    login: async function(){
      if (this.email === undefined || this.password === undefined){
        alert("Fields cannot be empty");
      }
      else{
        const res = await fetch('HTTP://127.0.0.1:5000/loginapi',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"email":this.email,"password":this.password})
    });
    //console.log(res,"sjjjjjjjjjjjjjj",res.json());
    if (res.status == 200){
      let data = await res.json()
      if (data != null){
        localStorage.setItem('token', data["token"])
        this.$router.push('/dashboard')
      }
    }
    else{
      alert('Incorrect username or password, please sign up if you have not signed up');
    }
  }
      },
    reverse: function(){
      this.message = this.message.split('').reverse().join('')
    }
  }

}
const Dashboard = {
  template:`
<div class='container'>
<p> Welcome username, You are logged in! </p>
<div class="card" class="shadow p-3 mb-5 bg-body rounded" style="background-color:lightblue;width: 18rem;">
<div class="card-body">
<h5 class="card-title">English</h5>
<p class="card-text">There are  English_number cards in this deck</p>
<p class="card-text">per_easy_english of users found this deck to be easy.</p>
<p class="card-text">per_difficult_english% of users found this deck to be difficult.</p>
<button @click="route_readcard('English')" class="btn btn-primary">Read/Add Cards</button>
</div>
</div>
`,
data: function(){
  return{
    username: undefined,
    password : undefined
  }
},
methods:{
  login: async function(){
    if (this.email === undefined || this.password === undefined){
      alert("Fields cannot be empty");
    }
    else{
      const res = await fetch('HTTP://127.0.0.1:5000/loginapi',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"email":this.email,"password":this.password})
  });
  //console.log(res,"sjjjjjjjjjjjjjj",res.json());
  if (res.status == 200){
    let data = await res.json()
    if (data != null){
      localStorage.setItem('token', data["token"])
      this.$router.push('/dashboard')
    }
  }
  else{
    alert('Incorrect username or password, please sign up if you have not signed up');
  }
}
    },
  reverse: function(){
    this.message = this.message.split('').reverse().join('')
  }
}
}
const routes = [
  { path: '/', component: LoginPage },
  { path: '/dashboard', component: Dashboard },
  // {path: '/newdeckform', component: AddDeck},
  // {path: '/readcard/:deck', component: ReadCard},
  // {path: '/:deck/cardform', component:CardForm},
  // {path:'/:deck/:front/:back/updatecardform', component: UpdateCardForm},
  {path:'/signup', component: SignUp}
]

const router = VueRouter.createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: VueRouter.createWebHashHistory(),
  routes, // short for `routes: routes`
})

// 5. Create and mount the root instance.
const app = Vue.createApp({
  data() {
    return {

    }
  },
  methods:{
    dashboard_redirect: function(){
      this.$router.push('/dashboard');
    },
    logout_user: function(){
      localStorage.removeItem('token');
    }
  }
})
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router)

app.mount('#app')
