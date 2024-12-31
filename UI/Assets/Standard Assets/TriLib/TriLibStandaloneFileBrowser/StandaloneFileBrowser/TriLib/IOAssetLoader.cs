#pragma warning disable 184

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TriLibCore.Mappers;
using TriLibCore.SFB;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore
{
    public class IOAssetLoader : MonoBehaviour
    {
        protected bool AutoDestroy;

        protected Action<AssetLoaderContext> OnLoad;
        protected Action<AssetLoaderContext> OnMaterialsLoad;
        protected Action<AssetLoaderContext, float> OnProgress;
        protected Action<IContextualizedError> OnError;
        protected Action<bool> OnBeginLoad;
        protected GameObject WrapperGameObject;
        protected AssetLoaderOptions AssetLoaderOptions;
        protected bool HaltTask;

        private IList<ItemWithStream> _items;
        private string _modelExtension;

        protected void DestroyMe()
        {
            Destroy(gameObject);
        }

        private void HandleFileLoading()
        {
            StartCoroutine(DoHandleFileLoading());
        }

        private IEnumerator DoHandleFileLoading()
        {
            var hasFiles = _items != null && _items.Count > 0 && _items[0].HasData;
            OnBeginLoad?.Invoke(hasFiles);
            yield return new WaitForEndOfFrame();
            yield return new WaitForEndOfFrame();
            if (!hasFiles)
            {
                if (AutoDestroy)
                {
                    DestroyMe();
                }
                yield break;
            }
            var modelFileWithStream = FindModelFile();
            var modelFilename = modelFileWithStream.Name;
            var modelStream = modelFileWithStream.OpenStream();
            if (AssetLoaderOptions == null)
            {
                AssetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
            }
            if (!ArrayUtils.ContainsType<FilePickerTextureMapper>(AssetLoaderOptions.TextureMappers))
            {
                AssetLoaderOptions.TextureMappers = new TextureMapper[] { ScriptableObject.CreateInstance<FilePickerTextureMapper>() };
            }
            if (!(AssetLoaderOptions.ExternalDataMapper is FilePickerExternalDataMapper))
            {
                AssetLoaderOptions.ExternalDataMapper = ScriptableObject.CreateInstance<FilePickerExternalDataMapper>();
            }
            _modelExtension = modelFilename != null ? FileUtils.GetFileExtension(modelFilename, false) : null;
            if (_modelExtension == "zip")
            {
                if (modelStream != null)
                {
                    AssetLoaderZip.LoadModelFromZipStream(modelStream, OnLoad, OnMaterialsLoad, OnProgress, OnError, WrapperGameObject, AssetLoaderOptions, CustomDataHelper.CreateCustomDataDictionaryWithData(_items), null, false, modelFilename);
                }
                else
                {
                    AssetLoaderZip.LoadModelFromZipFile(modelFilename, OnLoad, OnMaterialsLoad, OnProgress, OnError, WrapperGameObject, AssetLoaderOptions, CustomDataHelper.CreateCustomDataDictionaryWithData(_items), null);
                }
            }
            else
            {
                if (modelStream != null)
                {
                    AssetLoader.LoadModelFromStream(modelStream, modelFilename, _modelExtension, OnLoad, OnMaterialsLoad, OnProgress, OnError, WrapperGameObject, AssetLoaderOptions, CustomDataHelper.CreateCustomDataDictionaryWithData(_items), HaltTask);
                }
                else
                {
                    AssetLoader.LoadModelFromFile(modelFilename, OnLoad, OnMaterialsLoad, OnProgress, OnError, WrapperGameObject, AssetLoaderOptions, CustomDataHelper.CreateCustomDataDictionaryWithData(_items), HaltTask);
                }
            }
            if (AutoDestroy)
            {
                DestroyMe();
            }
        }

        protected static ExtensionFilter[] GetExtensions()
        {
            var extensions = Readers.Extensions;
            var extensionFilters = new List<ExtensionFilter>();
            var subExtensions = new List<string>();
            for (var i = 0; i < extensions.Count; i++)
            {
                var extension = extensions[i];
                extensionFilters.Add(new ExtensionFilter(null, extension));
                subExtensions.Add(extension);
            }

            subExtensions.Add("zip");
            extensionFilters.Add(new ExtensionFilter(null, new[] { "zip" }));
            extensionFilters.Add(new ExtensionFilter("All Files", new[] { "*" }));
            extensionFilters.Insert(0, new ExtensionFilter("Accepted Files", subExtensions.ToArray()));
            return extensionFilters.ToArray();
        }

        private ItemWithStream FindModelFile()
        {
            if (_items.Count == 1)
            {
                return _items.First();
            }
            var extensions = Readers.Extensions;
            for (var i = 0; i < _items.Count; i++)
            {
                var item = _items[i];
                if (item.Name == null)
                {
                    continue;
                }

                var extension = FileUtils.GetFileExtension(item.Name, false);
                if (extensions.Contains(extension))
                {
                    return item;
                }
            }

            return null;
        }

        protected void OnItemsWithStreamSelected(IList<ItemWithStream> itemsWithStream)
        {
            if (itemsWithStream != null)
            {
                _items = itemsWithStream;
                Dispatcher.InvokeAsync(HandleFileLoading);
            }
            else
            {
                if (AutoDestroy)
                {
                    DestroyMe();
                }
            }
        }

    }
}