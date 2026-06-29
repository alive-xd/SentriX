import re

with open(r"x:\Sentrix\frontend\app\assets\page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove Mock Data
content = re.sub(r'// ─── Mock Data ───.*?// ─── Helpers ───', '// ─── Helpers ───', content, flags=re.DOTALL)

# Remove TYPE_COUNTS
content = re.sub(r'const TYPE_COUNTS: Record<AssetType, number> = \{.*?\};', '', content, flags=re.DOTALL)

# Replace useQuery for assets
new_query = """  const { data: statsData } = useQuery({
    queryKey: ["assets-stats"],
    queryFn: async () => {
      const res = await assetsService.getStats();
      return res.data;
    }
  });

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["assets", search, assetType, criticality, owner, location, page],
    queryFn: async () => {
      const params: any = {
        skip: page * 50,
        limit: 50,
      };
      if (search) params.search = search;
      if (assetType) params.asset_type = assetType;
      if (criticality) params.criticality = criticality;
      if (owner) params.owner = owner;
      if (location) params.location = location;
      
      const res = await assetsService.getAll(params);
      return res.data;
    },
  });"""

content = re.sub(r'const { data, isLoading, refetch } = useQuery\(\{.*?\n  \}\);', new_query, content, flags=re.DOTALL)

# Replace `const stats = MOCK_STATS;`
content = content.replace("const stats = MOCK_STATS;", "const stats = statsData;")

# Replace `setPreview(a as MockAsset)` with `setPreview(a as Asset)`
content = content.replace("a as MockAsset", "a as Asset")
content = content.replace("MockAsset", "Asset")

# Replace `const count = TYPE_COUNTS[t] ?? 0;`
content = content.replace("const count = TYPE_COUNTS[t] ?? 0;", "const count = 0; // TODO: from stats if available")

with open(r"x:\Sentrix\frontend\app\assets\page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
