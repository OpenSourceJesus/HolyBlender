using System.IO;
using Stride.Engine;
using Stride.Core.Diagnostics;

using var game = new Game();
// FileStream file = File.Open();
Logger logger = GlobalLogger.RegisteredLoggers[1];
logger.Info("YAY");
game.Run();
