#pragma warning disable CS0105
using UnityEngine;
using TriLibCore.Interfaces;
using UnityEditor;
using TriLibCore.Utils;
using UnityEditor.AssetImporters;
namespace TriLibCore.Editor
{
    public class TriLibScriptedImporter : ScriptedImporter
    {
        public AssetLoaderOptions AssetLoaderOptions
        {
            get
            {
                var assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(true, true);
                if (userData != null && userData != "null")
                {
                    EditorJsonUtility.FromJsonOverwrite(userData, assetLoaderOptions);
                }
                //Editor coroutines are not allowed
                assetLoaderOptions.UseCoroutines = false;
                //Asset Unloader is not suitable for editor loading
                assetLoaderOptions.AddAssetUnloader = false;
                return assetLoaderOptions;
            }
            set => userData = EditorJsonUtility.ToJson(value);
        }

        public override void OnImportAsset(AssetImportContext assetImportContext)
        {
            var assetLoaderOptions = AssetLoaderOptions;
            assetLoaderOptions.Timeout = EditorPrefs.GetInt("TriLibTimeout", 180);
            var assetLoaderContext = AssetLoader.LoadModelFromFileNoThread(assetImportContext.assetPath, OnError, null, assetLoaderOptions, CustomDataHelper.CreateCustomDataDictionaryWithData(assetImportContext));
            if (assetLoaderContext.RootGameObject != null)
            {
                assetImportContext.AddObjectToAsset("Main", assetLoaderContext.RootGameObject);
                assetImportContext.SetMainObject(assetLoaderContext.RootGameObject);
                for (var i = 0; i < assetLoaderContext.Allocations.Count; i++)
                {
                    var allocation = assetLoaderContext.Allocations[i];
                    if (string.IsNullOrWhiteSpace(allocation.name))
                    {
                        allocation.name = allocation.GetType().Name;
                    }
                    assetImportContext.AddObjectToAsset(allocation.name, allocation);
                }
            }
        }

        private static void OnError(IContextualizedError contextualizedError)
        {
            var exception = contextualizedError.GetInnerException();
            if (contextualizedError.GetContext() is IAssetLoaderContext assetLoaderContext)
            {
                var assetImportContext = CustomDataHelper.GetCustomData<AssetImportContext>(assetLoaderContext.Context.CustomData);
                if (assetImportContext != null)
                {
                    assetImportContext.LogImportError(exception.ToString());
                    return;
                }
            }
            Debug.LogError(exception.ToString());
        }
    }
}