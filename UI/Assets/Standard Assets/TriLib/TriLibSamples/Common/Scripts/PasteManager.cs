using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace TriLibCore.Samples
{
    /// <summary>Represents a Class used to add paste capabilities to WebGL projects.</summary>
    public class PasteManager : MonoBehaviour
    {
#if UNITY_WEBGL && !UNITY_EDITOR
		[DllImport("__Internal")]
		private static extern void PasteManagerSetup();
#endif

        /// <summary>The Paste Manager Singleton instance.</summary>
        public static PasteManager Instance { get; private set; }

        /// <summary>Checks if the Singleton instance exists.</summary>
        public static void CheckInstance()
        {
            if (Instance == null)
            {
                Instance = new GameObject("PasteManager").AddComponent<PasteManager>();
            }
        }

#if UNITY_WEBGL && !UNITY_EDITOR
        private void Start()
		{
			PasteManagerSetup();
		}
#endif

        /// <summary>Called when the user pastes the given value in the Web-Browser.</summary>
		/// <param name="value">The pasted value.</param>
        public void Paste(string value)
        {
            var currentCurrentSelectedGameObject = EventSystem.current.currentSelectedGameObject;
            if (currentCurrentSelectedGameObject != null)
            {
                var inputField = currentCurrentSelectedGameObject.GetComponentInChildren<InputField>();
                if (inputField != null)
                {
                    var newText = $"{inputField.text.Substring(0, inputField.selectionAnchorPosition)}{value}{inputField.text.Substring(inputField.selectionFocusPosition)}";
                    inputField.text = newText;
                }
            }
        }
    }
}