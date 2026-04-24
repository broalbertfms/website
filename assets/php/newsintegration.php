<?php
// Query Loop Block Template for WordPress
$args = array(
    'post_type' => 'post',
    'posts_per_page' => 10, // Change as needed
);
$query = new WP_Query($args);

if ($query->have_posts()) : ?>
    <section class="wp-block-query-loop">
        <div class="posts-list">
            <?php while ($query->have_posts()) : $query->the_post(); ?>
                <article class="post-item">
                    <header>
                        <h2 class="post-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h2>
                        <div class="post-meta">
                            <span class="post-date"><?php echo get_the_date(); ?></span>
                            <span class="post-author">By <?php the_author(); ?></span>
                        </div>
                    </header>
                    <div class="post-excerpt">
                        <p><?php echo get_the_excerpt(); ?></p>
                    </div>
                    <footer>
                        <a href="<?php the_permalink(); ?>" class="read-more">Read More</a>
                    </footer>
                </article>
            <?php endwhile; ?>
        </div>
    </section>
    <?php wp_reset_postdata(); ?>
<?php else : ?>
    <p>No posts found.</p>
<?php endif; ?>