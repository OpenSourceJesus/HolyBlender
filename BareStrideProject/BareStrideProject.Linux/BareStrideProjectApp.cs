using Stride.Engine;
using Stride.Core.Mathematics;
using Stride.Core.Diagnostics;
using Stride.Core.Serialization;

using var game = new Game();
Logger logger = GlobalLogger.RegisteredLoggers[1];
logger.Info("YAY");
Async async = new Async();
Entity entity = new Entity("Entity Added by Script");
entity.Add(async);

// game.SceneSystem.SceneInstance.RootScene.Entities.Add(entity);
// async.Execute ();

game.Run();
game.SceneSystem.SceneInstance.RootScene.Entities.Add(entity);
