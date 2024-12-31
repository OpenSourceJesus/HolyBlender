#pragma warning disable 618

using System;
using TriLibCore.SFB;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore
{
    /// <summary>Represents an Asset Loader which loads files using a platform-specific file picker.</summary>
    public class AssetLoaderFilePicker : IOAssetLoader
    {
        /// <summary>Creates the Asset Loader File Picker Singleton instance.</summary>
        /// <returns>The created AssetLoaderFilePicker.</returns>
        public static AssetLoaderFilePicker Create()
        {
            var gameObject = new GameObject("AssetLoaderFilePicker");
            var assetLoaderFilePicker = gameObject.AddComponent<AssetLoaderFilePicker>();
            assetLoaderFilePicker.AutoDestroy = true;
            return assetLoaderFilePicker;
        }

        /// <summary>Loads a Model from the OS file picker asynchronously, or synchronously when the OS doesn't support Threads.</summary>
        /// <param name="title">The dialog title.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when the Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when the Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when the Model loading progress changes.</param>
        /// <param name="onBeginLoad">The Method to call when the model begins to load.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the model immediately and chain the Tasks.</param>
        public void LoadModelFromFilePickerAsync(string title, Action<AssetLoaderContext> onLoad, Action<AssetLoaderContext> onMaterialsLoad, Action<AssetLoaderContext, float> onProgress, Action<bool> onBeginLoad, Action<IContextualizedError> onError, GameObject wrapperGameObject, AssetLoaderOptions assetLoaderOptions, bool haltTask = false)
        {
            OnLoad = onLoad;
            OnMaterialsLoad = onMaterialsLoad;
            OnProgress = onProgress;
            OnError = onError;
            OnBeginLoad = onBeginLoad;
            WrapperGameObject = wrapperGameObject;
            AssetLoaderOptions = assetLoaderOptions;
            HaltTask = haltTask;
            try
            {
				StandaloneFileBrowser.OpenFilePanelAsync(title, null, GetExtensions(), true, OnItemsWithStreamSelected);
            }
            catch (Exception)
            {
                Dispatcher.InvokeAsync(DestroyMe);
                throw;
            }
        }
    }
}
