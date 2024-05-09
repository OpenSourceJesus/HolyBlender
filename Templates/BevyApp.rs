use bevy::prelude::*;
use bevy_asset_loader::prelude::*;
use bevy_gltf_components::ComponentsFromGltfPlugin;
use bevy_registry_export::*;

fn main() {
    App::new()
        ꗈ0
        .add_plugins((
            DefaultPlugins,
            ExportRegistryPlugin::default(),
            ComponentsFromGltfPlugin::default(),
        ))
        .init_state::<MyStates>()
        .add_loading_state(
            LoadingState::new(MyStates::AssetLoading)
                .continue_to_state(MyStates::Next)
                // .load_collection::<LevelAssets>(),
        )
        .add_systems(OnEnter(MyStates::Next), start_level)
        ꗈ1
        .run();
}

// #[derive(AssetCollection, Resource)]
// struct LevelAssets {
//     #[asset(path = "Test.glb#Scene.001")]
//     level: Handle<Scene>,
// }

fn start_level(
    mut commands: Commands,
    // assets: Res<LevelAssets>,
    mut meshes : ResMut<Assets<Mesh>>
) {
    ꗈ2

    // commands.spawn((
    //     SceneBundle {
    //         scene: assets.level.clone(),
    //         ..default()
    //     },
    //     Name::new("Test"),
    // ));
}

#[derive(
    Clone, Eq, PartialEq, Debug, Hash, Default, States,
)]
enum MyStates {
    #[default]
    AssetLoading,
    Next,
}
