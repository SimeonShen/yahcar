'use strict';

/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller, io } = app;

  io.of('/').route("sub_user_message",io.controller.visited.server);
  io.of('/').route("getaddr",io.controller.visited.getaddr);
  io.of('/').route("radar",io.controller.visited.radar);
  router.get('/', controller.renderHTML.index);
  router.get('/control', controller.renderHTML.control);
  router.get('/wander', controller.renderHTML.wander);
  router.get('/inforlist', controller.renderHTML.inforlist);
  router.get('/manual', controller.renderHTML.manual);
};
