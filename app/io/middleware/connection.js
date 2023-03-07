module.exports = (app) => {
  return async (ctx, next) => {
    // 通知全体
    console.log('success connection')
    
    ctx.socket.emit("res", "connected!");
    
    await next();
    // execute when disconnect.
    console.log("disconnection!");
  };
};
