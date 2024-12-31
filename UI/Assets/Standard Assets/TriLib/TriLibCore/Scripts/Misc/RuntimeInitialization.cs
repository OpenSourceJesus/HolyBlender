using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore
{
    /// <summary>
    /// Represents a class to initialize runtime components.
    /// </summary>
    public class RuntimeInitialization : MonoBehaviour
    {
        /// <summary>
        /// Initialize the runtime components used by TriLib.
        /// You can comment lines in this call and call them manually later if you don't want the component to be initialized automatically.
        /// </summary>
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        public static void Initialize()
        {
            Dispatcher.CheckInstance();
        }
    }
}
