using System;
using TriLibCore.Interfaces;
using TriLibCore.Mappers;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a UserPropertiesMapper that uses a callback when any User Property is processed.
    /// </summary>
    public class SampleUserPropertiesMapper : UserPropertiesMapper
    {
        /// <summary>
        /// The callback to call when any User Property is processed.
        /// </summary>
        public Action<GameObject, string, object> OnUserDataProcessed;
        
        public override void OnProcessUserData(AssetLoaderContext assetLoaderContext, GameObject gameObject, string propertyName, object propertyValue)
        {
            if (OnUserDataProcessed != null)
            {
                OnUserDataProcessed(gameObject, propertyName, propertyValue);
            }
        }
    }
}
