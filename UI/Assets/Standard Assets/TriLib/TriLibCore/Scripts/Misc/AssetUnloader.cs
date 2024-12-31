using System.Collections.Generic;
using UnityEngine;
namespace TriLibCore
{
    /// <summary>Represents a Class to destroy every Asset (Textures, Materials, Meshes) loaded by TriLib for this GameObject.</summary>
    public class AssetUnloader : MonoBehaviour
    {
        /// <summary>
        /// Assets Allocation List.
        /// </summary>
        public List<Object> Allocations;

        /// <summary>The Asset Unloader unique identifier.</summary>
        public int Id
        {
            get => _id;
            set
            {
                _id = value;
                Register();
            }
        }

        /// <summary>
        /// Custom data used to load the model.
        /// </summary>
        public object CustomData;

        [SerializeField]
        [HideInInspector]
        private int _id;

        private static int _lastId;

        private static readonly Dictionary<int, int> AssetUnloaders = new Dictionary<int, int>();

        /// <summary>Gets the next allocation Identifier.</summary>
        /// <returns>The Allocation Identifier.</returns>
        public static int GetNextId()
        {
            return _lastId++;
        }

        /// <summary>
        /// Returns whether there is any AssetUnloader instance active.
        /// </summary>
        public static bool HasRegisteredUnloaders
        {
            get
            {
                return AssetUnloaders.Count > 0;
            }
        }

        private void Register()
        {
            if (!AssetUnloaders.ContainsKey(_id))
            {
                AssetUnloaders[_id] = 0;
            }
            else
            {
                AssetUnloaders[_id]++;
            }
        }

        private void Start()
        {
            Register();
        }

        private void OnDestroy()
        {
            if (AssetUnloaders.TryGetValue(_id, out var value))
            {
                if (--value <= 0)
                {
                    for (var i = 0; i < Allocations.Count; i++)
                    {
                        var allocation = Allocations[i];
                        if (allocation == null)
                        {
                            continue;
                        }

                        Destroy(allocation);
                    }

                    AssetUnloaders.Remove(_id);
                }
                else
                {
                    AssetUnloaders[_id] = value;
                }
            }
        }
    }
}
