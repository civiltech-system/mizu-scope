<template>
  <div ref="mapContainer" class="w-full h-full" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";

interface GeoJSON {
  type: string;
  features: Array<{
    type: string;
    geometry: { type: string; coordinates: number[] };
    properties: Record<string, unknown>;
  }>;
}

const props = defineProps<{ regions: GeoJSON }>();

const mapContainer = ref<HTMLElement | null>(null);
let map: unknown = null;

const COLORS: Record<string, string> = {
  soft:      "#3B82F6",
  medium:    "#22C55E",
  hard:      "#EAB308",
  very_hard: "#EF4444",
  unknown:   "#9CA3AF",
};

onMounted(async () => {
  const maplibregl = await import("maplibre-gl");

  map = new maplibregl.Map({
    container: mapContainer.value!,
    style: {
      version: 8,
      sources: {
        osm: {
          type: "raster",
          tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
          tileSize: 256,
          attribution: "© OpenStreetMap contributors",
        },
      },
      layers: [{ id: "osm", type: "raster", source: "osm" }],
    },
    center: [136.5, 36.5],
    zoom: 5,
  });

  (map as any).on("load", () => {
    if (props.regions) addLayers();
  });
});

function addLayers() {
  const m = map as any;
  if (!m || m.getSource("regions")) return;

  m.addSource("regions", {
    type: "geojson",
    data: props.regions,
    cluster: true,
    clusterMaxZoom: 8,
    clusterRadius: 50,
  });

  // クラスタ円
  m.addLayer({
    id: "clusters",
    type: "circle",
    source: "regions",
    filter: ["has", "point_count"],
    paint: {
      "circle-color": "#3B82F6",
      "circle-radius": ["step", ["get", "point_count"], 20, 10, 30, 30, 40],
      "circle-opacity": 0.75,
    },
  });

  m.addLayer({
    id: "cluster-count",
    type: "symbol",
    source: "regions",
    filter: ["has", "point_count"],
    layout: { "text-field": "{point_count_abbreviated}", "text-size": 13 },
    paint: { "text-color": "#ffffff" },
  });

  // 個別マーカー
  m.addLayer({
    id: "points",
    type: "circle",
    source: "regions",
    filter: ["!", ["has", "point_count"]],
    paint: {
      "circle-radius": 10,
      "circle-color": [
        "match", ["get", "water_type"],
        "soft",      COLORS.soft,
        "medium",    COLORS.medium,
        "hard",      COLORS.hard,
        "very_hard", COLORS.very_hard,
        COLORS.unknown,
      ],
      "circle-stroke-width": 2,
      "circle-stroke-color": "#ffffff",
    },
  });

  // ポップアップ
  m.on("click", "points", (e: any) => {
    const p = e.features[0].properties;
    const coords = e.features[0].geometry.coordinates.slice();
    new (maplibregl as any).Popup({ offset: 12 })
      .setLngLat(coords)
      .setHTML(`
        <div style="min-width:180px;padding:4px">
          <p style="font-weight:700;margin-bottom:4px">${p.name}</p>
          <p style="font-size:13px;color:#555">硬度: ${p.hardness ?? "不明"} mg/L</p>
          <p style="font-size:13px;color:#555">飲用: ${p.drinkable ? "可" : "要確認"}</p>
          <a href="/${p.slug}" style="color:#2563eb;font-size:13px;display:block;margin-top:6px">詳細を見る →</a>
        </div>
      `)
      .addTo(m);
  });

  m.on("mouseenter", "points", () => { m.getCanvas().style.cursor = "pointer"; });
  m.on("mouseleave", "points", () => { m.getCanvas().style.cursor = ""; });

  // クラスタクリックでズーム
  m.on("click", "clusters", (e: any) => {
    const [feature] = m.queryRenderedFeatures(e.point, { layers: ["clusters"] });
    m.getSource("regions").getClusterExpansionZoom(
      feature.properties.cluster_id,
      (err: unknown, zoom: number) => {
        if (err) return;
        m.easeTo({ center: feature.geometry.coordinates, zoom });
      }
    );
  });
}

watch(
  () => props.regions,
  (geojson) => {
    const m = map as any;
    if (!m) return;
    if (m.getSource("regions")) {
      m.getSource("regions").setData(geojson);
    } else if (m.loaded()) {
      addLayers();
    }
  }
);

onUnmounted(() => {
  (map as any)?.remove();
});
</script>
