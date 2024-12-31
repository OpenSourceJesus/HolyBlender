﻿#pragma warning disable 184

using System;
using System.IO;
using ICSharpCode.SharpZipLib.Zip;
using TriLibCore.General;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore
{
    /// <summary>Represents an Asset Loader class which works with Zip files.</summary>
    //todo: unify async loading.
    public static class AssetLoaderZip
    {
        /// <summary>
        /// Buffer size used to copy the zip file entries content.
        /// </summary>
        private const int ZipBufferSize = 4096;

        /// <summary>
        /// Called when all model resources have been loaded.
        /// </summary>
        /// <param name="assetLoaderContext">The asset loading context, containing callbacks and model loading data.</param>
        private static void OnMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            var zipLoadCustomContextData = CustomDataHelper.GetCustomData<ZipLoadCustomContextData>(assetLoaderContext.CustomData);
            if (zipLoadCustomContextData != null)
            {
                if (zipLoadCustomContextData.Stream != null)
                {
                    zipLoadCustomContextData.Stream.Close();
                }
                if (zipLoadCustomContextData.OnMaterialsLoad != null)
                {
                    zipLoadCustomContextData.OnMaterialsLoad(assetLoaderContext);
                }
            }
        }

        /// <summary>
        /// Called when any loading error occurs.
        /// </summary>
        /// <param name="contextualizedError">Thrown error containing an attached context.</param>
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

        /// <summary>Loads a model from the given Zip file path asynchronously.</summary>
        /// <param name="path">The Zip file path.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when the Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when the Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when the Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Model inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the model immediately and chain the Tasks.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        /// <returns>The asset loader context, containing model loading information and the output game object.</returns>
        public static AssetLoaderContext LoadModelFromZipFile(string path,
            Action<AssetLoaderContext> onLoad,
            Action<AssetLoaderContext> onMaterialsLoad,
            Action<AssetLoaderContext, float> onProgress,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null,
            bool haltTask = false,
            Action<AssetLoaderContext> onPreLoad = null)
        {
            Stream stream = null;
            var memoryStream = SetupZipModelLoading(onError, ref stream, path, ref assetLoaderOptions, ref fileExtension, out var zipFile, out var zipEntry);
            var customDataDic = (object)CustomDataHelper.CreateCustomDataDictionaryWithData(new ZipLoadCustomContextData
            {
                ZipFile = zipFile,
                ZipEntry = zipEntry,
                Stream = stream,
                OnError = onError,
                OnMaterialsLoad = onMaterialsLoad
            });
            if (customContextData != null)
            {
                CustomDataHelper.SetCustomData(ref customDataDic, customContextData);
            }
            return AssetLoader.LoadModelFromStream(memoryStream,
                path,
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

        /// <summary>Loads a model from the given Zip file Stream asynchronously.</summary>
        /// <param name="stream">The Stream containing the Zip data.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when the Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when the Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when the Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Model inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the model immediately and chain the Tasks.</param> /// 
        /// <param name="modelFilename">The Zip file path.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        /// <returns>The asset loader context, containing model loading information and the output game object.</returns>
        public static AssetLoaderContext LoadModelFromZipStream(Stream stream,
            Action<AssetLoaderContext> onLoad,
            Action<AssetLoaderContext> onMaterialsLoad,
            Action<AssetLoaderContext, float> onProgress,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null,
            bool haltTask = false,
            string modelFilename = null,
            Action<AssetLoaderContext> onPreLoad = null)
        {
            var memoryStream = SetupZipModelLoading(onError, ref stream, null, ref assetLoaderOptions, ref fileExtension, out var zipFile, out var zipEntry);
            var customDataDic = (object)CustomDataHelper.CreateCustomDataDictionaryWithData(new ZipLoadCustomContextData
            {
                ZipFile = zipFile,
                ZipEntry = zipEntry,
                Stream = stream,
                OnError = onError,
                OnMaterialsLoad = onMaterialsLoad
            });
            if (customContextData != null)
            {
                CustomDataHelper.SetCustomData(ref customDataDic, customContextData);
            }
            return AssetLoader.LoadModelFromStream(memoryStream,
                modelFilename,
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

        /// <summary>Loads a model from the given Zip file path synchronously.</summary>
        /// <param name="path">The Zip file path.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Model inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <returns>The asset loader context, containing model loading information and the output game object.</returns>
        public static AssetLoaderContext LoadModelFromZipFileNoThread(string path,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null)
        {
            Stream stream = null;
            var memoryStream = SetupZipModelLoading(onError, ref stream, path, ref assetLoaderOptions, ref fileExtension, out var zipFile, out var zipEntry);
            var customDataDic = (object)CustomDataHelper.CreateCustomDataDictionaryWithData(new ZipLoadCustomContextData
            {
                ZipFile = zipFile,
                ZipEntry = zipEntry,
                Stream = stream,
                OnError = onError
            });
            if (customContextData != null)
            {
                CustomDataHelper.SetCustomData(ref customDataDic, customContextData);
            }
            var assetLoaderContext = AssetLoader.LoadModelFromStreamNoThread(memoryStream,
                path,
                fileExtension,
                OnError,
                wrapperGameObject,
                assetLoaderOptions,
                customDataDic,
                true);
            stream.Close();
            return assetLoaderContext;
        }

        /// <summary>Loads a model from the given Zip file Stream synchronously.</summary>
        /// <param name="stream">The Stream containing the Zip data.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="fileExtension">The Model inside the Zip file extension. If <c>null</c> TriLib will try to find a suitable model format inside the Zip file.</param>
        /// <returns>The asset loader context, containing model loading information and the output game object.</returns>
        public static AssetLoaderContext LoadModelFromZipStreamNoThread(Stream stream,
            Action<IContextualizedError> onError,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            string fileExtension = null)
        {
            var memoryStream = SetupZipModelLoading(onError, ref stream, null, ref assetLoaderOptions, ref fileExtension, out var zipFile, out var zipEntry);
            var customDataDic = (object)CustomDataHelper.CreateCustomDataDictionaryWithData(new ZipLoadCustomContextData
            {
                ZipFile = zipFile,
                ZipEntry = zipEntry,
                Stream = stream,
                OnError = onError
            });
            if (customContextData != null)
            {
                CustomDataHelper.SetCustomData(ref customDataDic, customContextData);
            }
            var assetLoaderContext = AssetLoader.LoadModelFromStreamNoThread(memoryStream,
                null,
                fileExtension,
                OnError,
                wrapperGameObject,
                assetLoaderOptions,
                customDataDic,
                true);
            stream.Close();
            return assetLoaderContext;
        }

        /// <summary>Configures the Zip Model loading, adding the Zip External Data/Texture Mappers.</summary>
        /// <param name="onError">The method to execute when any error occurs.</param>
        /// <param name="stream">The Stream containing the Zip data.</param>
        /// <param name="path">The Zip file path.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="fileExtension">The Model inside the Zip file extension.</param>
        /// <param name="zipFile">The Zip file instance.</param>
        /// <param name="modelZipEntry">The model Zip entry inside the Zip file.</param>
        /// <returns>The model file data stream.</returns>
        private static Stream SetupZipModelLoading(Action<IContextualizedError> onError, ref Stream stream, string path, ref AssetLoaderOptions assetLoaderOptions, ref string fileExtension, out ZipFile zipFile, out ZipEntry modelZipEntry)
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
            if (stream == null)
            {
                stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read);
            }
            var validExtensions = Readers.Extensions;
            zipFile = new ZipFile(stream);
            Stream memoryStream = null;
            modelZipEntry = null;
            foreach (ZipEntry zipEntry in zipFile)
            {
                if (!zipEntry.IsFile)
                {
                    continue;
                }
                var checkingFileExtension = FileUtils.GetFileExtension(zipEntry.Name, false);
                if (fileExtension != null && checkingFileExtension == fileExtension)
                {
                    memoryStream = ZipFileEntryToStream(out fileExtension, zipEntry, zipFile);
                    modelZipEntry = zipEntry;
                }
                else if (validExtensions.Contains(checkingFileExtension))
                {
                    memoryStream = ZipFileEntryToStream(out fileExtension, zipEntry, zipFile);
                    modelZipEntry = zipEntry;
                    break;
                }
            }
            if (memoryStream == null)
            {
                var exception = new Exception("Unable to find a suitable model on the Zip file. Please inform a valid model file extension.");
                onError?.Invoke(new ContextualizedError<string>(exception, "Error"));
            }
            return memoryStream;
        }

        /// <summary>Copies the contents of a Zip file Entry into a Memory Stream.</summary>
        /// <param name="fileExtension">The Model inside the Zip file extension.</param>
        /// <param name="zipEntry">The Zip file Entry.</param>
        /// <param name="zipFile">The Zip file instance.</param>
        /// <returns>A memory stream with the zip file entry contents.</returns>
        public static Stream ZipFileEntryToStream(out string fileExtension, ZipEntry zipEntry, ZipFile zipFile)
        {
            var buffer = new byte[ZipBufferSize];
            var zipFileStream = zipFile.GetInputStream(zipEntry);
            var memoryStream = new MemoryStream(ZipBufferSize);
            ICSharpCode.SharpZipLib.Core.StreamUtils.Copy(zipFileStream, memoryStream, buffer);
            memoryStream.Seek(0, SeekOrigin.Begin);
            zipFileStream.Close();
            fileExtension = FileUtils.GetFileExtension(zipEntry.Name, false);
            return memoryStream;
        }
    }
}