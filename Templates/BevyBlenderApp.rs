use bevy::prelude::*;
use bevy_asset_loader::prelude::*;
use bevy_gltf_components::ComponentsFromGltfPlugin;
use bevy_registry_export::*;
use bevy::render::camera::RenderTarget;
use bevy::window::WindowRef;
use bevy::window::PrimaryWindow;

fn main() {
	let app = App::new()
		ꗈ0
		.add_plugins((
			DefaultPlugins,
			ExportRegistryPlugin::default(),
			ComponentsFromGltfPlugin::default()
		))
		.init_state::<MyStates>()
		.add_loading_state(
			LoadingState::new(MyStates::AssetLoading)
				.continue_to_state(MyStates::Next)
				.load_collection::<LevelAssets>(),
		)
		.add_systems(OnEnter(MyStates::Next), StartLevel)
		.add_systems(Update, SetCursorWorldPoint)
		ꗈ1
		.run();
}

#[derive(AssetCollection, Resource)]
struct LevelAssets {
	#[asset(path = "Game.glb#Scene0")]
	level: Handle<Scene>,
}

fn StartLevel (
	mut commands: Commands,
	assets: Res<LevelAssets>,
	assetServer: Res<AssetServer>,
	mut meshes : ResMut<Assets<Mesh>>,
	keys: Res<ButtonInput<KeyCode>>,
	mouseButtons: Res<ButtonInput<MouseButton>>
) {
	ꗈ2
    commands.spawn((Camera2dBundle::default(), WorldCursorCoords::default()));
	commands.spawn((
		SceneBundle {
			scene: assets.level.clone(),
			..default()
		},
		Name::new("Game"),
	));
}

#[derive(
	Clone, Eq, PartialEq, Debug, Hash, Default, States,
)]
enum MyStates {
	#[default]
	AssetLoading,
	Next,
}

#[derive(Component, Default)]
struct WorldCursorCoords(Vec2);

static mut cursorWorldPoint : Vec3 = Vec3::ZERO;

fn SetCursorWorldPoint (
    q_window_primary: Query<&Window, With<PrimaryWindow>>,
    q_window: Query<&Window>,
    mut q_camera: Query<(&Camera, &GlobalTransform, &mut WorldCursorCoords)>,
) {
    for (camera, camera_transform, mut worldcursor) in &mut q_camera {
        let window = match camera.target {
			RenderTarget::Window(WindowRef::Primary) => {
                q_window_primary.single()
            },
            RenderTarget::Window(WindowRef::Entity(e_window)) => {
                q_window.get(e_window).unwrap()
            },
            _ => {
                continue;
            }
        };
        if let Some(world_position) = window.cursor_position()
            .and_then(|cursor| camera.viewport_to_world(camera_transform, cursor))
            .map(|ray| ray.origin.truncate())
        {
			unsafe
			{
				cursorWorldPoint = Vec3::new(world_position.x, 0.0, -world_position.y);
			}
        }
    }
}