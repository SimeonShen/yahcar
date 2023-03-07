'use strict';

const { io } = require('../../public/socket.io');

const Controller = require('egg').Controller;

class VisitedController extends Controller {
  async server() {
    const { ctx } = this;
    const message = ctx.args[0];
    console.log('0');
    console.log('[socket]recv:', message);
    await ctx.socket.emit('choose', message);
  }

  async getaddr() {
    const { ctx } = this;
    const message = ctx.args[0];
    console.log(message);
    var namespace = this.app.io.of('/car').sockets;
    //console.log(namespace)
    for(var key in namespace)
    {
      var addr=namespace[key].handshake.address.split(":")[3]
      console.log(addr)
      if(addr!=null)
      {
        await ctx.socket.emit("cameraaddr","http://"+addr+":8080/?action=stream")
        return
      }
    }
  }

  async radar() {
    const { ctx } = this;
    console.log('[socket]recv:radar',ctx.args[0]);
    await this.app.io.of("/").emit("radardraw",ctx.args[0])
  }
}

module.exports = VisitedController;
