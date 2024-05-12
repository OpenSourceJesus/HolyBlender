using Stride.Engine;
using Stride.Core.Diagnostics;
using Stride.Core.Serialization;

using var game = new Game();
Logger logger = GlobalLogger.RegisteredLoggers[1];
logger.Info("YAY");
UrlReference<Scene> sceneUrlRef = new UrlReference<Scene>("MainScene");
var nextScene = await Content.LoadAsync(sceneUrlRef);
SceneSystem.SceneInstance.RootScene = nextScene;

game.Run();
