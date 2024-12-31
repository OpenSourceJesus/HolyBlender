using System.Collections;
using UnityEngine;

namespace TriLibCore
{
    /// <summary>
    /// Represents a class used to dispatch coroutines.
    /// </summary>
    public class CoroutineHelper : MonoBehaviour
    {
        private static CoroutineHelper _instance;

        /// <summary>
        /// Gets the coroutine helper instance.
        /// </summary>
        public static CoroutineHelper Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = new GameObject("Coroutine Helper").AddComponent<CoroutineHelper>();
                    _instance.hideFlags = HideFlags.DontSave;
                }
                return _instance;
            }
        }

        /// <summary>
        /// Runs an enumerable method.
        /// </summary>
        /// <param name="enumerator">The method to run.</param>
        public static void RunMethod(IEnumerator enumerator)
        {
            while (enumerator.MoveNext())
            {

            }
        }

        private void OnDestroy()
        {
            _instance = null;
        }
    }
}