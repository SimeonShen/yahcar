'use strict';

const Controller = require('egg').Controller;

class RenderHTMLController extends Controller {
  async index() {
    const { ctx } = this;
    await ctx.render('index.html');
  }
  async control() {
    const { ctx } = this;
    await ctx.render('control.html');
  }
  async wander() {
    const { ctx } = this;
    await ctx.render('wander.html');
  }
  async inforlist() {
    const { ctx } = this;
    await ctx.render('inforlist.html');
  }
  async manual() {
    const { ctx } = this;
    await ctx.render('manual.html');
  }
}

module.exports = RenderHTMLController;
