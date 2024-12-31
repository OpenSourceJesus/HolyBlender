﻿using System;
using System.Collections.Generic;
using System.IO;
using ICSharpCode.SharpZipLib.Zip;
using TriLibCore.Utils;

namespace TriLibCore.Mappers
{
    /// <summary>Represents a Mapper class used to load external data from Zip files.</summary>
    public class ZipFileExternalDataMapper : ExternalDataMapper
    {
        /// <inheritdoc />
        public override Stream Map(AssetLoaderContext assetLoaderContext, string originalFilename, out string finalPath)
        {
            var zipLoadCustomContextData = CustomDataHelper.GetCustomData<ZipLoadCustomContextData>(assetLoaderContext.CustomData);
            if (zipLoadCustomContextData == null)
            {
                throw new Exception("Missing custom context data.");
            }
            var zipFile = zipLoadCustomContextData.ZipFile;
            if (zipFile == null)
            {
                throw new Exception("Zip file instance is null.");
            }
            var shortFileName = FileUtils.GetShortFilename(originalFilename).ToLowerInvariant();
            foreach (ZipEntry zipEntry in zipFile)
            {
                if (!zipEntry.IsFile)
                {
                    continue;
                }
                var checkingFileShortName = FileUtils.GetShortFilename(zipEntry.Name).ToLowerInvariant();
                if (shortFileName == checkingFileShortName)
                {
                    finalPath = zipFile.Name;
                    string _;
                    return AssetLoaderZip.ZipFileEntryToStream(out _, zipEntry, zipFile);
                }
            }
            finalPath = null;
            return null;
        }
    }
}