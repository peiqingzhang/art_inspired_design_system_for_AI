import type { Meta, StoryObj } from '@storybook/react';
import Skeleton from './Skeleton';

const meta  : Meta<typeof Skeleton> = {
  title: 'Components/Skeleton',
  component: Skeleton,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Skeleton>;

export const Text: Story = { args={{ variant: 'text', lines: 3 }} };
export const Rectangular: Story = { args={{ variant: 'rectangular' }} };
export const Circular: Story = { args={{ variant: 'circular' }} };
