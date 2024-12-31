#pragma warning disable 672

using System;
using ICSharpCode.SharpZipLib.Zip;
using TriLibCore.General;
using TriLibCore.Utils;

namespace TriLibCore.Mappers
{
    /// <summary>Represents a Mapper used to load Textures from Zip files.</summary>
    public class ZipFileTextureMapper : TextureMapper
    {
        /// <inheritdoc />
        public override void Map(TextureLoadingContext textureLoadingContext)
        {
            var zipLoadCustomContextData = CustomDataHelper.GetCustomData<ZipLoadCustomContextData>(textureLoadingContext.Context.CustomData);
            if (zipLoadCustomContextData == null)
            {
                throw new Exception("Missing custom context data.");
            }
            var zipFile = zipLoadCustomContextData.ZipFile;
            if (zipFile == null)
            {
                throw new Exception("Zip file instance is null.");
            }
            if (string.IsNullOrWhiteSpace(textureLoadingContext.Texture.Filename))
            {
                if (textureLoadingContext.Context.Options.ShowLoadingWarnings)
                {
                    UnityEngine.Debug.LogWarning("Texture name is null.");
                }
                return;
            }
            var modelFilenameWithoutExtension = FileUtils.GetFilenameWithoutExtension(zipLoadCustomContextData.ZipEntry.Name).ToLowerInvariant();
            var textureShortName = FileUtils.GetShortFilename(textureLoadingContext.Texture.Filename).ToLowerInvariant();
            foreach (ZipEntry zipEntry in zipFile)
            {
                if (!zipEntry.IsFile)
                {
                    continue;
                }
                var checkingFileShortName = FileUtils.GetShortFilename(zipEntry.Name).ToLowerInvariant();
                var checkingFilenameWithoutExtension = FileUtils.GetFilenameWithoutExtension(zipEntry.Name).ToLowerInvariant();
                if (
                    TextureUtils.IsValidTextureFileType(checkingFileShortName) &&
                    textureLoadingContext.TextureType == TextureType.Diffuse && modelFilenameWithoutExtension == checkingFilenameWithoutExtension 
                    || textureShortName == checkingFileShortName)
                {
                    textureLoadingContext.Stream = AssetLoaderZip.ZipFileEntryToStream(out _, zipEntry, zipFile);
                }
            }
        }
    }
}