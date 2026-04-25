const { test, expect } = require("@playwright/test");

test.describe("DeepSeek V4 Paper site", () => {
  test("desktop homepage renders key SEO content and official resources", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/DeepSeek V4 Paper/i);
    await expect(page.locator("h1")).toHaveText("DeepSeek V4 Paper");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /DeepSeek V4 paper guide/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://deepseekv4paper.lol/");
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute("content", /PDF, Benchmarks, Official Links/i);
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /index,follow/i);
    await expect(page.getByText("This site is not affiliated with DeepSeek.")).toBeVisible();
    await expect(page.locator("#highlights .info-card")).toHaveCount(4);
    await expect(page.locator("#benchmarks .benchmark-card")).toHaveCount(4);
    await expect(page.locator("#resources .resource-card")).toHaveCount(6);
    await expect(page.locator('script[type="application/ld+json"]')).toHaveCount(4);
    await expect(page.locator("[data-verified-date]")).toContainText("April 24, 2026");

    const reportLink = page.getByRole("link", { name: "Open Technical Report" });
    await expect(reportLink).toHaveAttribute("href", /DeepSeek_V4\.pdf/);

    const officialLinksButton = page.getByRole("link", { name: "Browse Official Links" });
    await expect(officialLinksButton).toHaveAttribute("href", "https://mirofish.my/");
    await expect(officialLinksButton).toHaveAttribute("target", "_blank");
    await expect(officialLinksButton).toHaveAttribute("rel", "noreferrer noopener");

    for (const image of await page.locator("img").all()) {
      await image.scrollIntoViewIfNeeded();
    }

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout stays within viewport and keeps sections navigable", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await page.getByRole("link", { name: "Resources" }).click();
    await expect(page.locator("#resources")).toBeInViewport();
    await page.getByRole("link", { name: "FAQ" }).click();
    await expect(page.locator("#faq")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await expect(page.locator(".resource-card")).toHaveCount(6);
    await context.close();
  });
});
