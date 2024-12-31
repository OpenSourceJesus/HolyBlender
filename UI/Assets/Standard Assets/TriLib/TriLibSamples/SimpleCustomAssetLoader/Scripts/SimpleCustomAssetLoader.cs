#pragma warning disable 672

using System;
using System.IO;
using TriLibCore.Interfaces;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// Custom external data mapper which works with callbacks.
    /// </summary>
    public class SimpleExternalDataMapper : ExternalDataMapper
    {
        private Func<string, Stream> _streamReceivingCallback;
        private Func<string, string> _finalPathReceivingCallback;

        public void Setup(Func<string, Stream> streamReceivingCallback, Func<string, string> finalPathReceivingCallback)
        {
            if (streamReceivingCallback == null)
            {
                throw new Exception("Callback parameter is missing.");
            }
            _streamReceivingCallback = streamReceivingCallback;
            _finalPathReceivingCallback = finalPathReceivingCallback;
        }

        public override Stream Map(AssetLoaderContext assetLoaderContext, string originalFilename, out string finalPath)
        {
            finalPath = _finalPathReceivingCallback != null ? _finalPathReceivingCallback(originalFilename) : originalFilename;
            return _streamReceivingCallback(originalFilename);
        }
    }

    /// <summary>
    /// Custom texture mapper which works with callbacks.
    /// </summary>
    public class SimpleTextureMapper : TextureMapper
    {
        private Func<ITexture, Stream> _streamReceivingCallback;

        public void Setup(Func<ITexture, Stream> streamReceivingCallback)
        {
            if (streamReceivingCallback == null)
            {
                throw new Exception("Callback parameter is missing.");
            }
            _streamReceivingCallback = streamReceivingCallback;
        }

        public override void Map(TextureLoadingContext textureLoadingContext)
        {
            var stream = _streamReceivingCallback(textureLoadingContext.Texture);
            textureLoadingContext.Stream = stream;
        }
    }

    /// <summary>
    /// Represents a class used to load models from Byte Arrays using callbacks to map External Data and Textures.
    /// </summary>
    public class SimpleCustomAssetLoader
    {
        /// <summary>
        /// Loads a model from the given Byte Array data using the given callbacks to handle events/external data.
        /// </summary>
        /// <param name="data">The model data Byte Array.</param>
        /// <param name="modelExtension">The model file extension.</param>
        /// <param name="onError">The error event callback (optional).</param>
        /// <param name="onProgress">The loading progress event callback.</param>
        /// <param name="onModelFullyLoad">The model loading event callback.</param>
        /// <param name="customDataReceivingCallback">The event that returns a Stream to read the external data passed to it.</param>
        /// <param name="customFilenameReceivingCallback">The event that returns a file-system complete filename from the filename passed to it (optional).</param>
        /// <param name="customTextureReceivingCallback">The event that returns a Stream to read Texture data from the filename passed to it.</param>
        /// <param name="modelFilename">The model filename (optional).</param>
        /// <param name="wrapperGameObject">The GameObject to wrap the loaded model (optional).</param>
        /// <param name="assetLoaderOptions">The AssetLoaderOptions to use when loading the model (optional).</param>
        /// <param name="customData">Any custom data to pass to the loading method, which can be retrieved later (optional).</param>
        /// <returns>The AssetLoaderContext containing all common data regarding the model loading.</returns>
        public static AssetLoaderContext LoadModelFromByteData(
            byte[] data,
            string modelExtension,
            Action<IContextualizedError> onError,
            Action<AssetLoaderContext, float> onProgress,
            Action<AssetLoaderContext> onModelFullyLoad,
            Func<string, Stream> customDataReceivingCallback,
            Func<string, string> customFilenameReceivingCallback,
            Func<ITexture, Stream> customTextureReceivingCallback,
            string modelFilename = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customData = null)
        {
            if (data == null || data.Length == 0)
            {
                throw new Exception("Missing model file byte data.");
            }
            return LoadModelFromStream(new MemoryStream(data), modelExtension, onError, onProgress, onModelFullyLoad, customDataReceivingCallback, customFilenameReceivingCallback, customTextureReceivingCallback, modelFilename, wrapperGameObject, assetLoaderOptions, customData);
        }

        /// <summary>
        /// Loads a model from the given Byte Array data using the given callbacks to handle events/external data.
        /// </summary>
        /// <param name="stream">The model data Stream.</param>
        /// <param name="modelExtension">The model file extension.</param>
        /// <param name="onError">The error event callback (optional).</param>
        /// <param name="onProgress">The loading progress event callback.</param>
        /// <param name="onModelFullyLoad">The model loading event callback.</param>
        /// <param name="customDataReceivingCallback">The event that returns a Stream to read the external data passed to it.</param>
        /// <param name="customFilenameReceivingCallback">The event that returns a file-system complete filename from the filename passed to it (optional).</param>
        /// <param name="customTextureReceivingCallback">The event that returns a Stream to read Texture data from the filename passed to it.</param>
        /// <param name="modelFilename">The model filename (optional).</param>
        /// <param name="wrapperGameObject">The GameObject to wrap the loaded model (optional).</param>
        /// <param name="assetLoaderOptions">The AssetLoaderOptions to use when loading the model (optional).</param>
        /// <param name="customData">Any custom data to pass to the loading method, which can be retrieved later (optional).</param>
        /// <returns>The AssetLoaderContext containing all common data regarding the model loading.</returns>
        public static AssetLoaderContext LoadModelFromStream(
            Stream stream,
            string modelExtension,
            Action<IContextualizedError> onError,
            Action<AssetLoaderContext, float> onProgress,
            Action<AssetLoaderContext> onModelFullyLoad,
            Func<string, Stream> customDataReceivingCallback,
            Func<string, string> customFilenameReceivingCallback,
            Func<ITexture, Stream> customTextureReceivingCallback,
            string modelFilename = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customData = null)
        {
            if (stream == null)
            {
                throw new Exception("Missing model file byte data.");
            }
            if (string.IsNullOrWhiteSpace(modelExtension) && !string.IsNullOrWhiteSpace(modelFilename))
            {
                modelExtension = FileUtils.GetFileExtension(modelFilename);
            }
            if (string.IsNullOrWhiteSpace(modelExtension))
            {
                throw new Exception("Missing model extension parameter");
            }
            var simpleExternalDataMapper = ScriptableObject.CreateInstance<SimpleExternalDataMapper>();
            simpleExternalDataMapper.Setup(customDataReceivingCallback, customFilenameReceivingCallback);
            var simpleTextureMapper = ScriptableObject.CreateInstance<SimpleTextureMapper>();
            simpleTextureMapper.Setup(customTextureReceivingCallback);
            if (assetLoaderOptions == null)
            {
                assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions();
            }
            assetLoaderOptions.ExternalDataMapper = simpleExternalDataMapper;
            assetLoaderOptions.TextureMappers = new TextureMapper[] { simpleTextureMapper};
            return AssetLoader.LoadModelFromStream(stream, modelFilename, modelExtension, null, onModelFullyLoad, onProgress, onError, wrapperGameObject, assetLoaderOptions, customData);
        }
    }
}
