#pragma warning disable 184

using System;
using System.IO;
using ICSharpCode.SharpZipLib.Zip;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore
{
    /// <summary>
    /// Represents a class used to load all the models inside a Zip file.
    /// </summary>
    public static class MultipleAssetLoaderZip
    {
        /// <summary>Loads all models from the given Zip file Stream asynchronously.</summary>
        /// <param name="stream">The Zip file Stream.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when any Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when any Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when any Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Objects. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Models.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Models inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the models immediately and chain the Tasks.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        public static void LoadAllModelsFromZipStream(
            Stream stream,
            Action<AssetLoaderContext> onLoad,
            Action<AssetLoaderContext> onMaterialsLoad,
            Action<AssetLoaderContext, float> onProgress,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null,
            bool haltTask = false,
            Action<AssetLoaderContext> onPreLoad = null
        )
        {
            if (assetLoaderOptions == null)
            {
                assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions();
            }
            SetupModelLoading(assetLoaderOptions);
            LoadModelsInternal(onLoad, onMaterialsLoad, onProgress, onError, wrapperGameObject, assetLoaderOptions, customContextData, fileExtension, haltTask, onPreLoad, stream);
        }

        /// <summary>Loads all models from the given Zip file path asynchronously.</summary>
        /// <param name="path">The Zip file path.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when any Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when any Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when any Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Objects. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Models.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Models inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the models immediately and chain the Tasks.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        public static void LoadAllModelsFromZipFile(
            string path,
            Action<AssetLoaderContext> onLoad,
            Action<AssetLoaderContext> onMaterialsLoad,
            Action<AssetLoaderContext, float> onProgress,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null,
            bool haltTask = false,
            Action<AssetLoaderContext> onPreLoad = null
        )
        {
            if (!File.Exists(path))
            {
                throw new Exception("File not found");
            }
            var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read);
            SetupModelLoading(assetLoaderOptions);
            LoadModelsInternal(onLoad, onMaterialsLoad, onProgress, onError, wrapperGameObject, assetLoaderOptions, customContextData, fileExtension, haltTask, onPreLoad, stream);
        }

        private static void SetupModelLoading(AssetLoaderOptions assetLoaderOptions)
        {
            if (assetLoaderOptions == null)
            {
                assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions();
            }
            if (!ArrayUtils.ContainsType<ZipFileTextureMapper>(assetLoaderOptions.TextureMappers))
            {
                assetLoaderOptions.TextureMappers = new TextureMapper[] { ScriptableObject.CreateInstance<ZipFileTextureMapper>() };
            }
            if (!(assetLoaderOptions.ExternalDataMapper is ZipFileExternalDataMapper))
            {
                assetLoaderOptions.ExternalDataMapper = ScriptableObject.CreateInstance<ZipFileExternalDataMapper>();
            }
        }

        private static void LoadModelsInternal(Action<AssetLoaderContext> onLoad,
            Action<AssetLoaderContext> onMaterialsLoad,
            Action<AssetLoaderContext, float> onProgress,
            Action<IContextualizedError> onError,
            GameObject wrapperGameObject,
            AssetLoaderOptions assetLoaderOptions,
            object customContextData,
            string fileExtension,
            bool haltTask,
            Action<AssetLoaderContext> onPreLoad,
            Stream stream)
        {
            var validExtensions = Readers.Extensions;
            var zipFile = new ZipFile(stream);
            foreach (ZipEntry zipEntry in zipFile)
            {
                if (!zipEntry.IsFile)
                {
                    continue;
                }

                Stream memoryStream = null;
                var checkingFileExtension = FileUtils.GetFileExtension(zipEntry.Name, false);
                if (fileExtension != null && checkingFileExtension == fileExtension)
                {
                    memoryStream = AssetLoaderZip.ZipFileEntryToStream(out fileExtension, zipEntry, zipFile);
                }
                else if (validExtensions.Contains(checkingFileExtension))
                {
                    memoryStream = AssetLoaderZip.ZipFileEntryToStream(out fileExtension, zipEntry, zipFile);
                }
                var customDataDic = (object)CustomDataHelper.CreateCustomDataDictionaryWithData(new ZipLoadCustomContextData
                {
                    ZipFile = zipFile,
                    Stream = stream,
                    OnError = onError,
                    OnMaterialsLoad = onMaterialsLoad
                });
                if (customContextData != null)
                {
                    CustomDataHelper.SetCustomData(ref customDataDic, customContextData);
                }
                if (memoryStream != null)
                {
                    AssetLoader.LoadModelFromStream(
                        memoryStream,
                        zipEntry.Name,
                        fileExtension,
                        onLoad,
                        OnMaterialsLoad,
                        onProgress,
                        OnError,
                        wrapperGameObject,
                        assetLoaderOptions,
                        customDataDic,
                        haltTask,
                        onPreLoad,
                        true);
                }
            }
            if (assetLoaderOptions.CloseStreamAutomatically)
            {
                stream.Close();
            }
        }

        //Todo: make the AssetLoaderZip method public and use that instead
        private static void OnMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            var zipLoadCustomContextData = CustomDataHelper.GetCustomData<ZipLoadCustomContextData>(assetLoaderContext.CustomData);
            if (zipLoadCustomContextData != null)
            {
                if (zipLoadCustomContextData.OnMaterialsLoad != null)
                {
                    zipLoadCustomContextData.OnMaterialsLoad(assetLoaderContext);
                }
            }
        }

        //Todo: make the AssetLoaderZip method public and use that instead
        private static void OnError(IContextualizedError contextualizedError)
        {
            if (contextualizedError?.GetContext() is AssetLoaderContext assetLoaderContext)
            {
                var zipLoadCustomContextData = CustomDataHelper.GetCustomData<ZipLoadCustomContextData>(assetLoaderContext.CustomData);
                if (zipLoadCustomContextData != null)
                {
                    if (zipLoadCustomContextData.Stream != null)
                    {
                        zipLoadCustomContextData.Stream.Close();
                    }
                    if (zipLoadCustomContextData.OnError != null)
                    {
                        zipLoadCustomContextData.OnError.Invoke(contextualizedError);
                    }
                }
            }
        }
    }
}