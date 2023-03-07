module.exports = (app) => {
  // socket接收到参数的预处理
  return async (ctx, next) => {
    //console.log(ctx.packet);
    await next();
    // execute when disconnect.
    console.log("socket 收到了些参数都会走这里!");
  };
};
