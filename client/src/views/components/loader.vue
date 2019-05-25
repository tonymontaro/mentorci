<template>
  <div class="cssload-jumping">
    <span></span>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
  </div>
</template>

<script>
export default {
  name: "loader"
};
</script>

<style>
.cssload-jumping {
  position: fixed;
  top: 30px;
  left: 45vw;
  display: block;
  margin: 10px auto;
  width: 107px;
  z-index: 999;
}

.cssload-jumping,
.cssload-jumping * {
  box-sizing: border-box;
}

.cssload-jumping span {
  display: inline-block;
  height: 15px;
  width: 15px;
  background: rgb(47, 172, 155);
  border-radius: 487px;
  background-clip: padding-box;
  -o-background-clip: padding-box;
  -ms-background-clip: padding-box;
  -webkit-background-clip: padding-box;
  -moz-background-clip: padding-box;
}

.cssload-jumping span:nth-child(1) {
  animation: scale 1.15s 0.12s infinite cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -o-animation: scale 1.15s 0.12s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -ms-animation: scale 1.15s 0.12s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -webkit-animation: scale 1.15s 0.12s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -moz-animation: scale 1.15s 0.12s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
}
.cssload-jumping span:nth-child(2) {
  animation: scale 1.15s 0.23s infinite cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -o-animation: scale 1.15s 0.23s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -ms-animation: scale 1.15s 0.23s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -webkit-animation: scale 1.15s 0.23s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -moz-animation: scale 1.15s 0.23s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
}
.cssload-jumping span:nth-child(3) {
  animation: scale 1.15s 0.35s infinite cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -o-animation: scale 1.15s 0.35s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -ms-animation: scale 1.15s 0.35s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -webkit-animation: scale 1.15s 0.35s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -moz-animation: scale 1.15s 0.35s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
}
.cssload-jumping span:nth-child(4) {
  animation: scale 1.15s 0.46s infinite cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -o-animation: scale 1.15s 0.46s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -ms-animation: scale 1.15s 0.46s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -webkit-animation: scale 1.15s 0.46s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -moz-animation: scale 1.15s 0.46s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
}
.cssload-jumping span:nth-child(5) {
  animation: scale 1.15s 0.58s infinite cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -o-animation: scale 1.15s 0.58s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -ms-animation: scale 1.15s 0.58s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -webkit-animation: scale 1.15s 0.58s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
  -moz-animation: scale 1.15s 0.58s infinite
    cubic-bezier(0.6, -0.28, 0.735, 0.045);
}

@keyframes scale {
  0% {
    transform: scale(0);
  }
  25% {
    transform: scale(0.9, 0.9);
    background: rgb(147, 225, 215);
  }
  50% {
    transform: scale(1, 1);
    margin: 0 3px;
    background: rgb(47, 172, 155);
  }
  100% {
    transform: scale(0);
  }
}

@-o-keyframes scale {
  0% {
    -o-transform: scale(0);
  }
  25% {
    -o-transform: scale(0.9, 0.9);
    background: rgb(147, 225, 215);
  }
  50% {
    -o-transform: scale(1, 1);
    margin: 0 3px;
    background: rgb(47, 172, 155);
  }
  100% {
    -o-transform: scale(0);
  }
}

@-ms-keyframes scale {
  0% {
    -ms-transform: scale(0);
  }
  25% {
    -ms-transform: scale(0.9, 0.9);
    background: rgb(147, 225, 215);
  }
  50% {
    -ms-transform: scale(1, 1);
    margin: 0 3px;
    background: rgb(47, 172, 155);
  }
  100% {
    -ms-transform: scale(0);
  }
}

@-webkit-keyframes scale {
  0% {
    -webkit-transform: scale(0);
  }
  25% {
    -webkit-transform: scale(0.9, 0.9);
    background: rgb(147, 225, 215);
  }
  50% {
    -webkit-transform: scale(1, 1);
    margin: 0 3px;
    background: rgb(47, 172, 155);
  }
  100% {
    -webkit-transform: scale(0);
  }
}

@-moz-keyframes scale {
  0% {
    -moz-transform: scale(0);
  }
  25% {
    -moz-transform: scale(0.9, 0.9);
    background: rgb(147, 225, 215);
  }
  50% {
    -moz-transform: scale(1, 1);
    margin: 0 3px;
    background: rgb(47, 172, 155);
  }
  100% {
    -moz-transform: scale(0);
  }
}
</style>
